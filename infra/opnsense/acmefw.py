#!/usr/bin/env python3
"""Configure ACME-FW through the OPNsense API. Idempotent; run on the PVE host.

ACME's public block is 198.51.100.10-15 on the fake internet. Each public IP is 1:1 NATed
to one DMZ server, so from outside participants see several "internet" hosts.

Scenario switches (disabled rules, toggle live in the GUI or with toggle-scenario.sh):
  "SCENARIO visitor" - lab and VPN can reach ACME LAN (someone plugged into a meeting room socket)
  "SCENARIO flat"    - every segment can reach every other (before segmentation)
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from opnapi import Opn  # noqa: E402

api = Opn("acme-fw")

# --- Legacy settings: no anti-lockout (LAN users must not reach the GUI), GUI on WAN only
api.php("""
$c = OPNsense\\Core\\Config::getInstance(); $o = $c->object();
$o->system->webgui->noantilockout = '1';
$o->system->webgui->interfaces = 'wan';
$c->save();
""")

api.gateway("WAN_GW", "wan", "198.51.100.1", default=True, descr="LAB-GW (internet)")
# Automatic outbound NAT only covers interfaces that have their gateway set on the interface
api.php("""
$c = OPNsense\\Core\\Config::getInstance(); $o = $c->object();
$o->interfaces->wan->gateway = 'WAN_GW';
$c->save();
""")
subprocess.run(["ssh", "acme-fw", "configctl interface reconfigure wan >/dev/null; configctl webgui restart >/dev/null; "
                "configctl filter reload >/dev/null"],
               check=True)

# --- Public IPs (IP aliases on WAN) and 1:1 NAT to the DMZ
PUBLIC = {  # name: (public, internal)
    "www": ("198.51.100.11", "172.20.10.11"),
    "shop": ("198.51.100.12", "172.20.10.12"),
    "mail": ("198.51.100.13", "172.20.10.13"),
    "ns1": ("198.51.100.14", "172.20.10.14"),
    "vpn": ("198.51.100.15", "172.20.10.15"),
}
for name, (pub, internal) in PUBLIC.items():
    api.upsert("interfaces/vip_settings", "Item", "descr", f"public {name}", {"vip": {
        "interface": "wan", "mode": "ipalias", "network": f"{pub}/24", "descr": f"public {name}"}})
api.call("/api/interfaces/vip_settings/reconfigure", {})
for seq, (name, (pub, internal)) in enumerate(PUBLIC.items(), start=1):
    api.upsert("firewall/one_to_one", "Rule", "description", f"1:1 {name}", {"rule": {
        "enabled": "1", "sequence": str(seq * 10), "interface": "wan", "type": "binat",
        "source_net": internal, "destination_net": "any", "external": pub,
        "description": f"1:1 {name}"}})
api.call("/api/firewall/one_to_one/apply", {})

# --- Aliases
api.aliases({
    "mgmt_ports": ("port", ["22", "8443"], "SSH and web GUI"),
    "web_ports": ("port", ["80", "443"], "HTTP and HTTPS"),
    "mail_ports": ("port", ["25", "110", "143", "587", "993"], "SMTP, POP3, IMAP"),
    "lab_nets": ("network", ["10.20.0.0/24", "10.20.100.0/24"], "Participants: Kali and VPN"),
    "acme_internal": ("network", ["172.20.10.0/24", "172.20.20.0/24", "172.20.30.0/24"], "All ACME segments"),
    "lab_proxy": ("host", ["198.51.100.1"], "LAB-GW Squid (updates)"),
})

# --- Filter rules. Interfaces: wan, opt1 = DMZ, lan = LAN, opt2 = IoT
ip = lambda name: PUBLIC[name][1]
api.rules([
    # WAN: management, published services, scenarios
    (10, "wan", "pass", "TCP", "172.31.255.1", "(self)", "mgmt_ports", "Management from PVE host"),
    (11, "wan", "pass", "ICMP", "any", "any", "", "WAN: ping"),
    (20, "wan", "pass", "TCP", "any", ip("www"), "web_ports", "Publish www"),
    (21, "wan", "pass", "TCP", "any", ip("shop"), "web_ports", "Publish shop"),
    (22, "wan", "pass", "TCP", "any", ip("mail"), "mail_ports", "Publish mail"),
    (23, "wan", "pass", "TCP/UDP", "any", ip("ns1"), "53", "Publish ns1"),
    (24, "wan", "pass", "TCP", "any", ip("vpn"), "22", "Publish vpn"),
    (80, "wan", "pass", "any", "lab_nets", "lan", "", "SCENARIO visitor", False),
    (81, "wan", "pass", "any", "lab_nets", "acme_internal", "", "SCENARIO flat (from outside)", False),
    # DMZ: DNS and updates; IoT reachable on purpose (finding for exercise 2.3)
    (100, "opt1", "pass", "TCP/UDP", "opt1", "(self)", "53", "DMZ: DNS"),
    (110, "opt1", "pass", "TCP", "opt1", "lab_proxy", "3128", "DMZ: updates via proxy"),
    (120, "opt1", "pass", "any", "opt1", "opt2", "", "DMZ: to IoT (misconfiguration)"),
    (180, "opt1", "pass", "any", "opt1", "acme_internal", "", "SCENARIO flat (DMZ)", False),
    (199, "opt1", "block", "any", "any", "any", "", "DMZ: default deny"),
    # LAN: employees may go anywhere (internet only through the proxy upstream)
    (200, "lan", "pass", "any", "lan", "any", "", "LAN: to any"),
    # IoT: DNS only
    (300, "opt2", "pass", "TCP/UDP", "opt2", "(self)", "53", "IoT: DNS"),
    (310, "opt2", "pass", "TCP", "opt2", "lab_proxy", "3128", "IoT: firmware updates via proxy"),
    (380, "opt2", "pass", "any", "opt2", "acme_internal", "", "SCENARIO flat (IoT)", False),
    (399, "opt2", "block", "any", "any", "any", "", "IoT: default deny"),
])

# --- DNS: acme.lab from ns1 (internal address), everything else via LAB-GW
for domain, server, descr in [("acme.lab", "172.20.10.14", "acme.lab from ns1"),
                              ("", "198.51.100.1", "Upstream: LAB-GW")]:
    api.upsert("unbound/settings", "Forward", "description", descr, {"dot": {
        "enabled": "1", "type": "forward", "domain": domain, "server": server, "port": "53",
        "description": descr}})
# ns1 answers with private addresses; allow them for acme.lab (otherwise unbound strips them)
api.saved("/api/unbound/settings/set", {"unbound": {"advanced": {"privatedomain": "acme.lab"}}})
api.call("/api/unbound/service/reconfigure", {})

print("acme-fw configured")
