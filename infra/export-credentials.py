#!/usr/bin/env python3
"""Export active participant credentials as a public, browser-decryptable bundle.

Claim codes stay in SECRETS/claim-codes.csv. Never exports the admin account.
Requires cryptography (see requirements-credentials.txt).
"""
import argparse
import base64
import csv
import hashlib
import json
import os
from pathlib import Path
import secrets
import tempfile

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

INFRA = Path(__file__).resolve().parent
ITERATIONS = 600_000
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def normalize(code):
    return "".join(code.upper().split()).replace("-", "")


def private_write(path, content):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def export(secrets_dir, output, rotate=False):
    with (secrets_dir / "participants.csv").open(newline="") as f:
        participants = [r for r in csv.DictReader(f)
                        if r["active"] == "yes" and r["access"] in ("kali", "wireguard")]
    # Validate/read all inputs before changing codes or public output.
    payloads = []
    for row in participants:
        user = row["user"]
        access = row["access"]
        expected = f"udelezenec{(100 if access == 'kali' else 200) + int(row['n'])}"
        if user != expected or not 1 <= int(row["n"]) <= 99:
            raise ValueError("Unexpected participant identity in CSV")
        payload = {"version": 1, "access": access, "user": user}
        if access == "kali":
            if not row["password"]:
                raise ValueError(f"Missing hosted password for {user}")
            payload.update(password=row["password"], url="https://lab.digilab-g.rtfm.si/")
        else:
            payload.update(filename=f"{user}.conf",
                           config=(secrets_dir / "wireguard" / f"{user}.conf").read_text())
            if "PrivateKey = " not in payload["config"]:
                raise ValueError(f"Invalid WireGuard config for {user}")
        payloads.append((row, json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()))

    codes_path = secrets_dir / "claim-codes.csv"
    codes = {}
    if codes_path.exists():
        with codes_path.open(newline="") as f:
            codes = {r["user"]: r for r in csv.DictReader(f)}
    for row in codes.values():
        row["active"] = "no"
    bundle = {"version": 1, "iterations": ITERATIONS, "entries": {}}
    for row, plaintext in payloads:
        user = row["user"]
        if rotate or user not in codes:
            code = "-".join("".join(secrets.choice(ALPHABET) for _ in range(5)) for _ in range(5))
            codes[user] = {"user": user, "access": row["access"], "claim_code": code}
        codes[user]["active"] = "yes"
        token = normalize(codes[user]["claim_code"]).encode()
        ident = hashlib.sha256(token).hexdigest()
        salt, iv = secrets.token_bytes(16), secrets.token_bytes(12)
        key = hashlib.pbkdf2_hmac("sha256", token, salt, ITERATIONS, dklen=32)
        aad = f"cybersec-201-access-v1:{ident}".encode()
        ciphertext = AESGCM(key).encrypt(iv, plaintext, aad)
        bundle["entries"][ident] = {
            key: base64.b64encode(value).decode()
            for key, value in (("salt", salt), ("iv", iv), ("ciphertext", ciphertext))
        }
    # Save private codes first: an interrupted export must not lose the only decryption keys.
    import io
    buf = io.StringIO()
    writer = csv.DictWriter(buf, ["user", "access", "claim_code", "active"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(codes.values())
    private_write(codes_path, buf.getvalue())
    output.parent.mkdir(parents=True, exist_ok=True)
    # Atomic replacement also prevents partially written bundles during a build.
    private_write(output, json.dumps(bundle, indent=2, sort_keys=True) + "\n")
    os.chmod(output, 0o644)
    return len(payloads)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--secrets", type=Path, default=INFRA / "secrets")
    parser.add_argument("--output", type=Path,
                        default=INFRA.parent / "cybersec-201/vaje/dostop/credentials.json")
    parser.add_argument("--rotate", action="store_true", help="Replace all active claim codes")
    args = parser.parse_args()
    count = export(args.secrets, args.output, args.rotate)
    print(f"Exported {count} encrypted participant entries to {args.output}")
    print(f"Private distribution list: {args.secrets / 'claim-codes.csv'} (not printed)")
