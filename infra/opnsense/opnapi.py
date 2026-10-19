"""Small OPNsense API client shared by the firewall configuration scripts.

Credentials: /root/.config/opn/NAME with three whitespace-separated values: key, secret, base URL.
"""
import json
import ssl
import subprocess
import sys
import time
import urllib.request
from base64 import b64encode


class Opn:
    def __init__(self, name):
        self.name = name
        key, secret, self.url = open(f"/root/.config/opn/{name}").read().split()
        self.auth = "Basic " + b64encode(f"{key}:{secret}".encode()).decode()
        self.ctx = ssl._create_unverified_context()

    def call(self, path, data=None):
        req = urllib.request.Request(self.url + path, method="POST" if data is not None else "GET")
        req.add_header("Authorization", self.auth)
        body = None
        if data is not None:
            req.add_header("Content-Type", "application/json")
            body = json.dumps(data).encode()
        with urllib.request.urlopen(req, body, context=self.ctx) as r:
            return json.load(r)

    def saved(self, path, data):
        res = self.call(path, data)
        if res.get("result") not in ("saved", "deleted") and res.get("status") != "ok":
            sys.exit(f"{self.name} {path}: {res}")
        return res

    def rows(self, path):
        return self.call(path, {"current": 1, "rowCount": -1, "searchPhrase": ""})["rows"]

    def upsert(self, base, kind, key, match, payload):
        """base='firewall/alias', kind='Item' -> searchItem/addItem/setItem; match row[key] == match."""
        for row in self.rows(f"/api/{base}/search{kind}"):
            if row.get(key) == match and not row.get("is_automatic"):
                self.saved(f"/api/{base}/set{kind}/{row['uuid']}", payload)
                return row["uuid"]
        return self.saved(f"/api/{base}/add{kind}", payload)["uuid"]

    def php(self, code):
        """Run PHP on the firewall over SSH (for legacy settings without an API)."""
        subprocess.run(["ssh", self.name, "php"], input="<?php\nrequire_once 'config.inc';\n" + code,
                       text=True, check=True)

    def aliases(self, aliases):
        """{name: (type, [content], description)}"""
        for name, (typ, content, descr) in aliases.items():
            self.upsert("firewall/alias", "Item", "name", name, {"alias": {
                "enabled": "1", "name": name, "type": typ, "content": "\n".join(content),
                "description": descr}})
        self.call("/api/firewall/alias/reconfigure", {})

    def rules(self, rules):
        """[(sequence, interface, action, protocol, source, destination, port, description[, enabled])]
        Rules are matched by description, so descriptions must be unique."""
        for seq, iface, action, proto, src, dst, port, descr, *rest in rules:
            enabled = rest[0] if rest else True
            self.upsert("firewall/filter", "Rule", "description", descr, {"rule": {
                "enabled": "1" if enabled else "0", "sequence": str(seq), "action": action, "quick": "1",
                "interface": iface, "direction": "in", "ipprotocol": "inet", "protocol": proto,
                "source_net": src, "destination_net": dst, "destination_port": port,
                "log": "1" if action == "block" else "0", "description": descr}})
        self.call("/api/firewall/filter/apply", {})

    def gateway(self, name, interface, address, default=False, descr=""):
        self.upsert("routing/settings", "Gateway", "name", name, {"gateway_item": {
            "name": name, "interface": interface, "ipprotocol": "inet", "gateway": address,
            "defaultgw": "1" if default else "0", "monitor_disable": "1", "descr": descr}})
        self.call("/api/routing/settings/reconfigure", {})
        # reconfigure is asynchronous; routes reject the gateway until it shows up as an option
        for _ in range(60):
            if name in self.call("/api/routes/routes/getroute")["route"]["gateway"]:
                return
            time.sleep(2)
        sys.exit(f"{self.name}: gateway {name} did not become available")
