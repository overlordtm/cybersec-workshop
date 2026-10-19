#!/usr/bin/env python3
"""Configure ACME-FW through the OPNsense API. Idempotent; run on the PVE host.

ACME's public block is 198.51.100.10-15 on the fake internet. Each public IP is 1:1 NATed
to one DMZ server, so from outside participants see several "internet" hosts.

Scenarios (internet / visitor / flat) are switched with scenario.py; see the README.
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
    "dmz_ports": ("port", ["22", "25", "53", "80", "110", "143", "443", "587", "993"],
                  "Services the DMZ offers (to the LAN and to visitors)"),
    "lab_nets": ("network", ["10.20.0.0/24", "10.20.100.0/24"], "Participants: Kali and VPN"),
    "acme_internal": ("network", ["172.20.10.0/24", "172.20.20.0/24", "172.20.30.0/24"], "All ACME segments"),
    "lab_proxy": ("host", ["198.51.100.1"], "LAB-GW Squid (updates)"),
})

# --- Filter rules. Interfaces: wan, opt1 = DMZ, lan = LAN, opt2 = IoT.
# Scenarios (see README "Scenarios"): rules named "SCENARIO <mode>: ..." are switched by
# scenario.py. LAB-GW only routes ACME's private ranges in the visitor and flat modes.
api.remove_rules(["SCENARIO visitor", "SCENARIO flat (from outside)", "SCENARIO flat (DMZ)",
                  "SCENARIO flat (IoT)", "LAN: to any"])
ip = lambda name: PUBLIC[name][1]
api.rules([
    # WAN: management, ping, published services (1:1 NAT: rules see the internal address)
    (10, "wan", "pass", "TCP", "172.31.255.1", "(self)", "mgmt_ports", "Management from PVE host"),
    (11, "wan", "pass", "ICMP", "any", "(self)", "", "WAN: ping firewall"),
    (12, "wan", "pass", "ICMP", "any", "opt1", "", "WAN: ping public servers"),
    (20, "wan", "pass", "TCP", "any", ip("www"), "web_ports", "Publish www"),
    (21, "wan", "pass", "TCP", "any", ip("shop"), "web_ports", "Publish shop"),
    (22, "wan", "pass", "TCP", "any", ip("mail"), "mail_ports", "Publish mail"),
    (23, "wan", "pass", "TCP/UDP", "any", ip("ns1"), "53", "Publish ns1"),
    (24, "wan", "pass", "TCP", "any", ip("vpn"), "22", "Publish vpn"),
    # visitor: participants get exactly what an office PC on the LAN gets (rules 200-220)
    (80, "wan", "pass", "any", "lab_nets", "lan", "", "SCENARIO visitor: like a LAN PC (LAN)", False),
    (81, "wan", "pass", "TCP/UDP", "lab_nets", "opt1", "dmz_ports", "SCENARIO visitor: like a LAN PC (DMZ services)", False),
    (82, "wan", "pass", "ICMP", "lab_nets", "opt1", "", "SCENARIO visitor: like a LAN PC (ping DMZ)", False),
    # flat: no segmentation at all
    (90, "wan", "pass", "any", "lab_nets", "acme_internal", "", "SCENARIO flat: outside to all segments", False),
    # DMZ: DNS and updates; IoT reachable on purpose (pivot finding: from a DMZ server to IoT)
    (100, "opt1", "pass", "TCP/UDP", "opt1", "(self)", "53", "DMZ: DNS"),
    (110, "opt1", "pass", "TCP", "opt1", "lab_proxy", "3128", "DMZ: updates via proxy"),
    (120, "opt1", "pass", "any", "opt1", "opt2", "", "DMZ: to IoT (misconfiguration)"),
    (180, "opt1", "pass", "any", "opt1", "acme_internal", "", "SCENARIO flat: DMZ to all segments", False),
    (199, "opt1", "block", "any", "any", "any", "", "DMZ: default deny"),
    # LAN: office PCs - DNS, DMZ services, internet; IoT is off limits
    (200, "lan", "pass", "TCP/UDP", "lan", "(self)", "53", "LAN: DNS"),
    (210, "lan", "pass", "TCP/UDP", "lan", "opt1", "dmz_ports", "LAN: DMZ services"),
    (211, "lan", "pass", "ICMP", "lan", "opt1", "", "LAN: ping DMZ"),
    (220, "lan", "pass", "any", "lan", "!acme_internal", "", "LAN: to the internet"),
    (280, "lan", "pass", "any", "lan", "acme_internal", "", "SCENARIO flat: LAN to all segments", False),
    (299, "lan", "block", "any", "any", "any", "", "LAN: default deny"),
    # IoT: DNS and firmware updates only
    (300, "opt2", "pass", "TCP/UDP", "opt2", "(self)", "53", "IoT: DNS"),
    (310, "opt2", "pass", "TCP", "opt2", "lab_proxy", "3128", "IoT: firmware updates via proxy"),
    (380, "opt2", "pass", "any", "opt2", "acme_internal", "", "SCENARIO flat: IoT to all segments", False),
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
