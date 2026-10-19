"""Cross-language crypto regression checks using dummy credentials only."""
import base64
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("credential_export", ROOT / "infra/export-credentials.py")
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class ExportTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.secrets = self.root / "secrets"
        (self.secrets / "wireguard").mkdir(parents=True)
        self.output = self.root / "public/credentials.json"
        self.password = "test-only-<&-password"
        self.config = "[Interface]\nPrivateKey = dummy-test-key\nAddress = 10.20.100.101/32\n"
        (self.secrets / "wireguard/udelezenec201.conf").write_text(self.config)
        self.rows = [
            {"n": "1", "user": "udelezenec101", "password": self.password, "access": "kali", "active": "yes"},
            {"n": "1", "user": "udelezenec201", "password": "", "access": "wireguard", "active": "yes"},
            {"n": "0", "user": "admin", "password": "admin-test-only", "access": "admin", "active": "yes"},
            {"n": "2", "user": "udelezenec102", "password": "inactive-test-only", "access": "kali", "active": "no"},
        ]
        self.write_participants()

    def write_participants(self):
        with (self.secrets / "participants.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, ["n", "user", "password", "access", "active"])
            w.writeheader()
            w.writerows(self.rows)

    def codes(self):
        with (self.secrets / "claim-codes.csv").open(newline="") as f:
            return {r["user"]: r for r in csv.DictReader(f)}

    def test_webcrypto_interop_wrong_code_and_tampering(self):
        self.assertEqual(exporter.export(self.secrets, self.output), 2)
        bundle = json.loads(self.output.read_text())
        codes = self.codes()
        self.assertEqual(set(codes), {"udelezenec101", "udelezenec201"})
        text = self.output.read_text()
        for value in (self.password, self.config, "admin-test-only", "inactive-test-only"):
            self.assertNotIn(value, text)
        for row in codes.values():
            self.assertNotIn(row["claim_code"], text)
            self.assertEqual(len(exporter.normalize(row["claim_code"])), 25)
        self.assertEqual((self.secrets / "claim-codes.csv").stat().st_mode & 0o777, 0o600)
        # Execute the same Web Crypto function imported by the actual browser page.
        script = '''
          import assert from 'node:assert/strict';
          import { readFileSync } from 'node:fs';
          import { createHash } from 'node:crypto';
          import { decryptCredential } from './cybersec-201/vaje/dostop/crypto.js';
          const {bundle, codes, password, config} = JSON.parse(readFileSync(0, 'utf8'));
          const kali = await decryptCredential(bundle, codes.udelezenec101.claim_code.toLowerCase().replaceAll('-', ' '));
          assert.equal(kali.access, 'kali');
          assert.equal(kali.password, password);
          const wg = await decryptCredential(bundle, codes.udelezenec201.claim_code);
          assert.equal(wg.config, config);
          assert.equal(wg.filename, 'udelezenec201.conf');
          assert.equal(wg.password, undefined);
          await assert.rejects(decryptCredential(bundle, 'invalid'));
          const id = createHash('sha256').update(codes.udelezenec101.claim_code.replaceAll('-', '')).digest('hex');
          const entry = bundle.entries[id];
          const bytes = Buffer.from(entry.ciphertext, 'base64');
          bytes[0] ^= 1;
          entry.ciphertext = bytes.toString('base64');
          await assert.rejects(decryptCredential(bundle, codes.udelezenec101.claim_code));
        '''
        subprocess.run(["node", "--input-type=module", "-e", script], cwd=ROOT,
                       input=json.dumps({"bundle": bundle, "codes": codes,
                                         "password": self.password, "config": self.config}),
                       text=True, capture_output=True, check=True)
        token = exporter.normalize(codes["udelezenec101"]["claim_code"]).encode()
        ident = hashlib.sha256(token).hexdigest()
        entry = bundle["entries"][ident]
        # A wrong AES key cannot authenticate the ciphertext even with a known lookup id.
        with self.assertRaises(InvalidTag):
            AESGCM(bytes(32)).decrypt(base64.b64decode(entry["iv"]),
                                      base64.b64decode(entry["ciphertext"]),
                                      f"cybersec-201-access-v1:{ident}".encode())

    def test_code_reuse_retirement_rotation_and_atomic_failure(self):
        exporter.export(self.secrets, self.output)
        original = self.codes()
        exporter.export(self.secrets, self.output)
        self.assertEqual(self.codes(), original)
        # Missing config must leave the previously published bundle and codes intact.
        previous = self.output.read_bytes()
        (self.secrets / "wireguard/udelezenec201.conf").unlink()
        with self.assertRaises(FileNotFoundError):
            exporter.export(self.secrets, self.output, rotate=True)
        self.assertEqual(self.codes(), original)
        self.assertEqual(self.output.read_bytes(), previous)
        self.rows[1]["active"] = "no"
        self.write_participants()
        exporter.export(self.secrets, self.output)
        self.assertEqual(len(json.loads(self.output.read_text())["entries"]), 1)
        self.assertEqual(self.codes()["udelezenec201"]["active"], "no")
        self.assertEqual(self.codes()["udelezenec101"]["claim_code"], original["udelezenec101"]["claim_code"])
        exporter.export(self.secrets, self.output, rotate=True)
        self.assertNotEqual(self.codes()["udelezenec101"]["claim_code"], original["udelezenec101"]["claim_code"])


if __name__ == "__main__":
    unittest.main()
