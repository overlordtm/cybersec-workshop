"""Local regression checks; no Proxmox or firewall access required."""
import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

GENERATOR = Path(__file__).resolve().parents[1] / "guacamole/gen-users.py"


class ParticipantsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.csv = self.root / "participants.csv"

    def generate(self, kali, wg):
        subprocess.run([sys.executable, "-I", str(GENERATOR), str(self.root),
                        str(self.root / "guac"), str(kali), str(wg)],
                       check=True, capture_output=True)
        with self.csv.open() as f:
            rows = list(csv.DictReader(f))
        xml = ET.parse(self.root / "guac/user-mapping.xml")
        return rows, {u.attrib["username"]: u for u in xml.getroot()}

    def test_independent_counts_resize_and_password_reuse(self):
        rows, users = self.generate(2, 3)
        self.assertEqual(set(users), {"admin", "udelezenec101", "udelezenec102"})
        self.assertEqual(len(users["admin"].findall("connection")), 2)
        wg = [r for r in rows if r["access"] == "wireguard"]
        self.assertEqual([r["user"] for r in wg],
                         ["udelezenec201", "udelezenec202", "udelezenec203"])
        self.assertTrue(all(r["password"] == "" for r in wg))
        original = {r["user"]: r["password"] for r in rows}
        rows, users = self.generate(4, 1)
        self.assertEqual(len(users), 5)  # Growing after admin exists must not skip a number.
        self.assertEqual(sum(r["access"] == "wireguard" and r["active"] == "yes"
                             for r in rows), 1)
        rows, users = self.generate(0, 0)
        self.assertEqual(set(users), {"admin"})
        self.assertEqual(users["admin"].findall("connection"), [])
        rows, _ = self.generate(2, 3)
        self.assertTrue(all(r["password"] == original[r["user"]]
                            for r in rows if r["user"] in original))

    def test_legacy_migration_and_xml_escaping(self):
        self.csv.write_text('n,user,password\n1,udelezenec01,a<&b\n0,admin,kept\n')
        rows, users = self.generate(2, 1)
        hosted = next(r for r in rows if r["user"] == "udelezenec101")
        self.assertEqual(hosted["password"], "a<&b")
        self.assertEqual(next(r["password"] for r in rows if r["user"] == "admin"), "kept")
        params = {p.attrib["name"]: p.text for p in users["udelezenec101"].findall("connection/param")}
        self.assertEqual(params["password"], "a<&b")
        self.assertEqual(params["hostname"], "10.20.0.101")

    def test_invalid_counts_do_not_modify_credentials(self):
        self.generate(1, 1)
        before = self.csv.read_bytes()
        for kali, wg in ((-1, 1), (100, 1), (1, 100), (1, -1), ("1.5", 0)):
            with self.assertRaises(subprocess.CalledProcessError):
                self.generate(kali, wg)
            self.assertEqual(self.csv.read_bytes(), before)



class WireGuardTest(unittest.TestCase):
    def test_configs_peers_and_revocation(self):
        """Execute the actual VPN provisioner with a fake API and temporary secrets."""
        from types import SimpleNamespace
        from unittest.mock import Mock
        import json
        import os

        source = (GENERATOR.parents[1] / "opnsense/labgw.py").read_text()
        vpn_code = source.split("# --- WireGuard for participants' own laptops (split tunnel: ACME only)\n", 1)[1]
        vpn_code = vpn_code.split("# Rules on the WireGuard interface group", 1)[0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "secrets/wireguard").mkdir(parents=True)
            config_dir = root / "secrets/wireguard"
            for name in ("udelezenec01", "udelezenec101", "udelezenec202"):
                (config_dir / f"{name}.conf").write_text("old")
            (root / "secrets/wg-keys.json").write_text(json.dumps({
                "_server": {"priv": "server-private", "pub": "server-public"},
                "admin": {"priv": "admin-private", "pub": "admin-public"},
            }))
            api = Mock()
            api.rows.side_effect = lambda path: (
                [{"name": "wg-lab", "pubkey": "server-public"}] if "searchServer" in path
                else [{"name": name, "uuid": name} for name in
                      ("udelezenec01", "udelezenec101", "udelezenec202", "custom-peer")])
            api.upsert.side_effect = lambda base, kind, key, name, payload: name
            process = Mock()
            process.run.side_effect = lambda *args, **kwargs: SimpleNamespace(stdout="test-key\n")
            context = {"json": json, "os": os, "subprocess": process, "api": api,
                       "WG_NET": "10.20.100", "WG_SERVER_IP": "10.20.100.1", "WG_PORT": "51820",
                       "PUBLIC_NAME": "example.test", "vpn": [
                           {"user": "udelezenec201", "n": "1", "access": "wireguard"},
                           {"user": "admin", "n": "0", "access": "admin"}]}
            exec(compile(vpn_code.replace("/root/lab", tmp), "vpn-provisioning", "exec"), context)
            self.assertEqual({p.name for p in config_dir.iterdir()}, {"udelezenec201.conf", "admin.conf"})
            self.assertIn("Address = 10.20.100.101/32", (config_dir / "udelezenec201.conf").read_text())
            self.assertIn("Address = 10.20.100.250/32", (config_dir / "admin.conf").read_text())
            server_call = next(c for c in api.upsert.call_args_list if c.args[0] == "wireguard/server")
            self.assertEqual(server_call.args[-1]["server"]["peers"], "udelezenec201,admin")
            self.assertEqual({c.args[0] for c in api.saved.call_args_list if "delClient" in c.args[0]},
                             {f"/api/wireguard/client/delClient/{name}" for name in
                              ("udelezenec01", "udelezenec101", "udelezenec202")})
            saved_keys = (root / "secrets/wg-keys.json").read_bytes()
            api.rows.side_effect = lambda path: ([{"name": "wg-lab", "pubkey": "server-public"}]
                                                 if "searchServer" in path else [])
            exec(compile(vpn_code.replace("/root/lab", tmp), "vpn-provisioning", "exec"), context)
            self.assertEqual((root / "secrets/wg-keys.json").read_bytes(), saved_keys)


if __name__ == "__main__":
    unittest.main()
