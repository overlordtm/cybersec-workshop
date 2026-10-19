#!/usr/bin/env python3
"""Turn a freshly generated OPNsense config.xml into a reachable bootstrap config.

Sets hostname, interfaces, root password and SSH key, an API key, moves the web GUI
to a different port and allows SSH and GUI from the management host on WAN.
Everything else is configured later through the API.

Usage: bootstrap.py PROFILE default.xml out.xml SECRETS_DIR
"""
import base64, copy, subprocess, sys, uuid
import xml.etree.ElementTree as ET

PROFILES = {
    "lab-gw": {
        "hostname": "lab-gw",
        "domain": "lab.internal",
        "secret_prefix": "labgw",
        "mgmt_host": "172.31.255.1",
        "gateway": "172.31.255.1",
        "interfaces": {
            # name: (device, ipaddr, subnet, description)
            "wan": ("vtnet0", "172.31.255.2", "30", "WAN"),
            "lan": ("vtnet1", "10.20.0.1", "24", "LAB"),
            "opt1": ("vtnet2", "198.51.100.1", "24", "FAKENET"),
        },
    },
    "acme-fw": {
        "hostname": "fw",
        "domain": "acme.lab",
        "secret_prefix": "acmefw",
        "mgmt_host": "172.31.255.1",
        "gateway": "198.51.100.1",
        "interfaces": {
            # Proxmox NIC order: net0 fakenet, net1 acmedmz, net2 acmelan, net3 acmeiot
            "wan": ("vtnet0", "198.51.100.10", "24", "WAN"),
            "lan": ("vtnet2", "172.20.20.1", "24", "LAN"),
            "opt1": ("vtnet1", "172.20.10.1", "24", "DMZ"),
            "opt2": ("vtnet3", "172.20.30.1", "24", "IOT"),
        },
    },
}

profile, src, dst, secrets = sys.argv[1:5]
P = PROFILES[profile]
read = lambda name: open(f"{secrets}/{name}").read().strip()

def crypt(pw):
    return subprocess.run(["openssl", "passwd", "-6", "-stdin"], input=pw, capture_output=True,
                          text=True, check=True).stdout.strip()

def setx(parent, tag, text=None):
    el = parent.find(tag)
    if el is None:
        el = ET.SubElement(parent, tag)
    if text is not None:
        el.text = text
    return el

tree = ET.parse(src)
root = tree.getroot()
for el in root.findall("trigger_initial_wizard"):
    root.remove(el)

system = root.find("system")
setx(system, "hostname", P["hostname"])
setx(system, "domain", P["domain"])
setx(system, "dnsallowoverride", "0")
setx(system, "dnsserver", "1.1.1.1")

user = system.find("user[name='root']")
setx(user, "password", crypt(read(f"{P['secret_prefix']}-root.pass")))
setx(user, "authorizedkeys", base64.b64encode(open(f"{secrets}/pve-lab.pub", "rb").read()).decode())
apikeys = setx(user, "apikeys")
for item in list(apikeys):
    apikeys.remove(item)
item = ET.SubElement(apikeys, "item")
setx(item, "key", read(f"{P['secret_prefix']}-api.key"))
setx(item, "secret", crypt(read(f"{P['secret_prefix']}-api.secret")))

webgui = system.find("webgui")
# Drop the GUI certificate of the source config; OPNsense creates a fresh one on boot
for el in webgui.findall("ssl-certref"):
    webgui.remove(el)
for el in root.findall("cert"):
    root.remove(el)
setx(webgui, "port", "8443")
setx(webgui, "disablehttpredirect", "1")
setx(webgui, "interfaces", "wan,lan")  # lan for later in-lab admin, filtered by rules

ssh = system.find("ssh")
setx(ssh, "enabled", "enabled")
setx(ssh, "permitrootlogin", "1")
setx(ssh, "passwordauth", "0")
setx(ssh, "interfaces", "wan")

ifaces = root.find("interfaces")
for name, (dev, ip, net, descr) in P["interfaces"].items():
    el = ifaces.find(name)
    if el is None:
        el = ET.SubElement(ifaces, name)
    for child in list(el):
        el.remove(child)
    for tag, val in [("enable", "1"), ("if", dev), ("descr", descr), ("ipaddr", ip), ("subnet", net),
                     ("spoofmac", ""), ("blockpriv", "0"), ("blockbogons", "0")]:
        setx(el, tag, val)

# Default gateway on WAN (without it the box cannot answer the management host)
gws = root.find("OPNsense/Gateways")
gw = ET.SubElement(gws, "gateway_item", uuid=str(uuid.uuid4()))
for tag, val in [("disabled", "0"), ("name", "WAN_GW"), ("descr", "Upstream"), ("interface", "wan"),
                 ("ipprotocol", "inet"), ("gateway", P["gateway"]), ("defaultgw", "1"), ("fargw", "0"),
                 ("monitor_disable", "1"), ("priority", "255"), ("weight", "1")]:
    setx(gw, tag, val)

# DHCP and IPv6 are configured later; drop the default LAN ranges
dnsmasq = root.find("dnsmasq")
for r in dnsmasq.findall("dhcp_ranges"):
    dnsmasq.remove(r)

# Firewall: keep only one rule — management from the host on WAN.
# Rules accept a single port or range only; lists need a port alias.
aliases = root.find("OPNsense/Firewall/Alias/aliases")
alias = ET.SubElement(aliases, "alias", uuid=str(uuid.uuid4()))
for tag, val in [("enabled", "1"), ("name", "mgmt_ports"), ("type", "port"), ("proto", ""), ("interface", ""),
                 ("counters", "0"), ("updatefreq", ""), ("content", "22\n8443"),
                 ("description", "SSH and web GUI")]:
    setx(alias, tag, val)

rules = root.find("OPNsense/Firewall/Filter/rules")
template = rules.find("rule")
for r in list(rules):
    rules.remove(r)
rule = copy.deepcopy(template)
rule.set("uuid", str(uuid.uuid4()))
for tag, val in [("sequence", "1"), ("interface", "wan"), ("protocol", "TCP"), ("source_net", P["mgmt_host"]),
                 ("destination_net", "(self)"), ("destination_port", "mgmt_ports"), ("log", "1"),
                 ("description", "Management from PVE host")]:
    setx(rule, tag, val)
rules.append(rule)

ET.indent(tree, "  ")
tree.write(dst, xml_declaration=True, encoding="utf-8")
