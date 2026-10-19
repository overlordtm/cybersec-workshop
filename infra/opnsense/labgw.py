#!/usr/bin/env python3
"""Configure LAB-GW through the OPNsense API. Idempotent; run on the PVE host.

Objects are matched by name (aliases, gateways) or description (rules, DHCP ranges, ...)
and updated in place, so the script can be re-run after every change.
Reads /root/lab/participants.csv; writes WireGuard client configs to /root/lab/secrets/wireguard/.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from opnapi import Opn  # noqa: E402

api = Opn("lab-gw")
PUBLIC_NAME = "lab.digilab-g.rtfm.si"

# --- Legacy settings without an API: outbound NAT off, no anti-lockout, GUI on WAN only.
# LAB-GW's own traffic leaves from 172.31.255.2; nothing from lab/VPN is ever NATed, so
# anything that slips through a rule is still dropped by the PVE host.
api.php("""
$c = OPNsense\\Core\\Config::getInstance(); $o = $c->object();
$o->nat->outbound->mode = 'disabled';
$o->system->webgui->noantilockout = '1';
$o->system->webgui->interfaces = 'wan';
$c->save();
""")
subprocess.run(["ssh", "lab-gw", "configctl webgui restart >/dev/null; configctl filter reload"], check=True)

# --- Gateways and routes
api.gateway("WAN_GW", "wan", "172.31.255.1", default=True, descr="PVE host")
api.gateway("ACME_GW", "opt1", "198.51.100.10", descr="ACME-FW")
api.upsert("routes/routes", "route", "descr", "ACME internal", {"route": {
    "network": "172.20.0.0/16", "gateway": "ACME_GW", "descr": "ACME internal", "enabled": "1"}})
api.call("/api/routes/routes/reconfigure", {})

# --- Aliases
api.aliases({
    "mgmt_ports": ("port", ["22", "8443"], "SSH and web GUI"),
    "web_ports": ("port", ["80", "443"], "HTTP and HTTPS (Caddy)"),
    "acme_nets": ("network", ["198.51.100.0/24", "172.20.0.0/16"], "ACME public and internal networks"),
    "acme_fw": ("host", ["198.51.100.10"], "ACME-FW WAN address"),
    "acme_public": ("network", ["198.51.100.8/29"], "ACME public block (.10 firewall, .11-.15 DMZ)"),
})

# --- Filter rules
WG_NET, WG_SERVER_IP, WG_PORT = "10.20.100", "10.20.100.1", "51820"
api.rules([
    (10, "wan", "pass", "TCP", "172.31.255.1", "(self)", "mgmt_ports", "Management from PVE host"),
    (11, "wan", "pass", "ICMP", "172.31.255.1", "any", "", "PVE host: ping"),
    (12, "wan", "pass", "TCP", "172.31.255.1", "acme_fw", "mgmt_ports", "PVE host: manage ACME-FW"),
    (20, "wan", "pass", "TCP", "any", "(self)", "web_ports", "Public: Caddy (Guacamole)"),
    (30, "wan", "pass", "UDP", "any", "(self)", WG_PORT, "Public: WireGuard"),
    (100, "lan", "pass", "TCP/UDP", "lan", "(self)", "53", "LAB: DNS"),
    (110, "lan", "pass", "TCP", "lan", "(self)", "3128", "LAB: web proxy"),
    (120, "lan", "pass", "ICMP", "lan", "(self)", "", "LAB: ping gateway"),
    (130, "lan", "pass", "any", "lan", "acme_nets", "", "LAB: to ACME"),
    (199, "lan", "block", "any", "lan", "any", "", "LAB: default deny"),
    (200, "opt1", "pass", "TCP/UDP", "opt1", "(self)", "53", "FAKENET: DNS"),
    (210, "opt1", "pass", "TCP", "acme_public", "(self)", "3128", "FAKENET: ACME-FW web proxy"),
    (220, "opt1", "pass", "ICMP", "opt1", "(self)", "", "FAKENET: ping gateway"),
    (299, "opt1", "block", "any", "any", "any", "", "FAKENET: default deny"),
])

# --- DHCP on LAB. Kali clones get MAC bc:24:11:20:00:NN (set by infra/kali/clones.sh).
api.upsert("dnsmasq/settings", "Range", "description", "LAB pool", {"range": {
    "interface": "lan", "start_addr": "10.20.0.200", "end_addr": "10.20.0.250",
    "domain_type": "range", "description": "LAB pool"}})
HOSTS = {"guacamole": ("10.20.0.10", ""), "greenbone": ("10.20.0.11", "")}
HOSTS.update({f"kali-{n:02d}": (f"10.20.0.{100 + n}", f"bc:24:11:20:00:{n:02d}") for n in range(1, 21)})
for name, (ip, mac) in HOSTS.items():
    api.upsert("dnsmasq/settings", "Host", "host", name, {"host": {
        "host": name, "domain": "lab.internal", "ip": ip, "hwaddr": mac, "descr": "lab"}})
api.call("/api/dnsmasq/service/reconfigure", {})

# --- DNS: acme.lab is answered by ACME's public name server (as on the real internet)
api.upsert("unbound/settings", "Forward", "description", "acme.lab from ns1", {"dot": {
    "enabled": "1", "type": "forward", "domain": "acme.lab", "server": "198.51.100.14", "port": "53",
    "description": "acme.lab from ns1"}})
api.saved("/api/unbound/settings/set", {"unbound": {"advanced": {"privatedomain": "acme.lab"}}})
api.call("/api/unbound/service/reconfigure", {})

# --- Squid: allowlist only (blacklist "." blocks everything, whitelist overrides it)
ALLOW = [
    # Kali and tooling
    "kali.org", "kali.download", "github.com", "githubusercontent.com", "github.io", "githubassets.com",
    "pypi.org", "pythonhosted.org", "rubygems.org",
    # ACME servers: Debian and Docker images
    "deb.debian.org", "security.debian.org", "archive.debian.org", "docker.io", "docker.com",
    # References for the exercises (CVE lookup, docs)
    "nvd.nist.gov", "cve.org", "cve.mitre.org", "cvedetails.com", "exploit-db.com",
    "owasp.org", "gchq.github.io",
]
api.saved("/api/proxy/settings/set", {"proxy": {
    "general": {"enabled": "1", "error_pages": "opnsense", "suppressVersion": "1"},
    "forward": {
        "interfaces": "lan,opt1", "port": "3128", "addACLforInterfaceSubnets": "1",
        "acl": {"whiteList": ",".join(ALLOW), "blackList": ".",
                "safePorts": "80:http,443:https", "sslPorts": "443:https"},
    },
}})
api.call("/api/proxy/service/reconfigure", {})
# reconfigure rewrites squid.conf but does not always reload the running Squid
subprocess.run(["ssh", "lab-gw", "configctl proxy restart >/dev/null"], check=True)

# --- WireGuard for participants' own laptops (split tunnel: ACME only)
KEYS = "/root/lab/secrets/wg-keys.json"
PARTICIPANTS = [r.split(",")[1] for r in open("/root/lab/participants.csv").read().split()[1:]]
keys = json.load(open(KEYS)) if os.path.exists(KEYS) else {}
for name in PARTICIPANTS:
    if name not in keys:
        priv = subprocess.run(["wg", "genkey"], capture_output=True, text=True, check=True).stdout.strip()
        pub = subprocess.run(["wg", "pubkey"], input=priv, capture_output=True, text=True, check=True).stdout.strip()
        keys[name] = {"priv": priv, "pub": pub}
os.makedirs(os.path.dirname(KEYS), mode=0o700, exist_ok=True)
secret_file = lambda path: open(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w")
with secret_file(KEYS) as f:
    json.dump(keys, f, indent=1)

peer_ip = lambda name: f"{WG_NET}.250" if name == "admin" else f"{WG_NET}.{100 + int(name[-2:])}"
peers = [api.upsert("wireguard/client", "Client", "name", name, {"client": {
    "enabled": "1", "name": name, "pubkey": keys[name]["pub"], "tunneladdress": f"{peer_ip(name)}/32",
    "keepalive": "25"}}) for name in PARTICIPANTS]

server = {"enabled": "1", "name": "wg-lab", "port": WG_PORT, "tunneladdress": f"{WG_SERVER_IP}/24",
          "disableroutes": "1", "peers": ",".join(peers)}
# The server key is kept with the client keys, so a rebuilt LAB-GW keeps the same client configs
if "_server" not in keys:
    existing = [r for r in api.rows("/api/wireguard/server/searchServer") if r["name"] == "wg-lab"]
    if existing:
        cur = api.call(f"/api/wireguard/server/getServer/{existing[0]['uuid']}")["server"]
        keys["_server"] = {"priv": cur["privkey"], "pub": cur["pubkey"]}
    else:
        kp = api.call("/api/wireguard/server/keyPair")
        keys["_server"] = {"priv": kp["privkey"], "pub": kp["pubkey"]}
    with secret_file(KEYS) as f:
        json.dump(keys, f, indent=1)
server.update(privkey=keys["_server"]["priv"], pubkey=keys["_server"]["pub"])
api.upsert("wireguard/server", "Server", "name", "wg-lab", {"server": server})
api.saved("/api/wireguard/general/set", {"general": {"enabled": "1"}})
api.call("/api/wireguard/service/reconfigure", {})
server_pub = next(r for r in api.rows("/api/wireguard/server/searchServer") if r["name"] == "wg-lab")["pubkey"]

os.makedirs("/root/lab/secrets/wireguard", mode=0o700, exist_ok=True)
for name in PARTICIPANTS:
    with secret_file(f"/root/lab/secrets/wireguard/{name}.conf") as f:
        f.write(f"[Interface]\n# ACME lab - {name}\nPrivateKey = {keys[name]['priv']}\n"
                f"Address = {peer_ip(name)}/32\nDNS = {WG_SERVER_IP}\n\n"
                f"[Peer]\nPublicKey = {server_pub}\nEndpoint = {PUBLIC_NAME}:{WG_PORT}\n"
                f"AllowedIPs = {WG_SERVER_IP}/32, 198.51.100.0/24, 172.20.0.0/16\nPersistentKeepalive = 25\n")

# Rules on the WireGuard interface group (exists only once WireGuard is enabled)
api.rules([
    (300, "wireguard", "pass", "TCP/UDP", f"{WG_NET}.0/24", WG_SERVER_IP, "53", "VPN: DNS"),
    (310, "wireguard", "pass", "ICMP", f"{WG_NET}.0/24", WG_SERVER_IP, "", "VPN: ping gateway"),
    (320, "wireguard", "pass", "any", f"{WG_NET}.0/24", "acme_nets", "", "VPN: to ACME"),
    (399, "wireguard", "block", "any", "any", "any", "", "VPN: default deny"),
])

# --- Caddy: public HTTPS (Let's Encrypt) -> Guacamole
api.saved("/api/caddy/General/set", {"caddy": {"general": {"enabled": "1"}}})
domain = api.upsert("caddy/ReverseProxy", "ReverseProxy", "FromDomain", PUBLIC_NAME, {"reverse": {
    "enabled": "1", "FromDomain": PUBLIC_NAME, "description": "Guacamole"}})
api.upsert("caddy/ReverseProxy", "Handle", "description", "Guacamole", {"handle": {
    "enabled": "1", "reverse": domain, "HandleType": "handle", "HandleDirective": "reverse_proxy",
    "ToDomain": "10.20.0.10", "ToPort": "8080", "description": "Guacamole"}})
api.call("/api/caddy/service/reconfigure", {})

print("lab-gw configured")
