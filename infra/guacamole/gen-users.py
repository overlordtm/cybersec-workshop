#!/usr/bin/env python3
"""Generate participant credentials and Guacamole's user-mapping.xml.

Usage: gen-users.py SECRETS_DIR OUT_DIR [KALI_COUNT] [WG_COUNT]
Credentials are kept in SECRETS_DIR/participants.csv (created once, then reused):
  n,user,password,access,active -- inactive credentials are retained for reuse.
Defaults: 15 hosted Kali accounts, 0 WireGuard participants.
"""
import csv, hashlib, os, secrets, sys
from xml.sax.saxutils import escape, quoteattr

secrets_dir, out_dir = sys.argv[1:3]
counts = [int(value) for value in sys.argv[3:5]]
kali_count = counts[0] if counts else 15
wg_count = counts[1] if len(counts) > 1 else 0
if not all(0 <= value <= 99 for value in (kali_count, wg_count)):
    sys.exit("Kali and WireGuard counts must be between 0 and 99")
os.makedirs(secrets_dir, mode=0o700, exist_ok=True)
path = f"{secrets_dir}/participants.csv"
words = "jabolko hruska sliva breskev marelica cesnja visnja jagoda malina robida".split()

rows = []
if os.path.exists(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
# Migrate the old shared accounts to hosted Kali, preserving desktop passwords.
for r in rows:
    if "access" not in r:
        r["access"] = "admin" if r["user"] == "admin" else "kali"
        if r["access"] == "kali":
            r["user"] = f"udelezenec{100 + int(r['n'])}"
    r["active"] = "no"
for access, count, base in (("kali", kali_count, 100), ("wireguard", wg_count, 200)):
    for n in range(1, count + 1):
        row = next((r for r in rows if r["access"] == access and int(r["n"]) == n), None)
        if row is None:
            pw = (f"{secrets.choice(words)}-{secrets.randbelow(9000) + 1000}-{secrets.token_hex(2)}"
                  if access == "kali" else "")
            row = {"n": str(n), "user": f"udelezenec{base + n}", "password": pw, "access": access}
            rows.append(row)
        row["active"] = "yes"
if not any(r["user"] == "admin" for r in rows):
    rows.append({"n": "0", "user": "admin", "password": secrets.token_urlsafe(16), "access": "admin"})
admin = next(r for r in rows if r["user"] == "admin")
admin["active"] = "yes"
with open(path, "w", newline="") as f:
    w = csv.DictWriter(f, ["n", "user", "password", "access", "active"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
os.chmod(path, 0o600)
participants = [r for r in rows if r["access"] == "kali" and r["active"] == "yes"]


def connection(r):
    n = int(r["n"])
    params = {
        "hostname": f"10.20.0.{100 + n}", "port": "3389", "username": "kali", "password": r["password"],
        "security": "any", "ignore-cert": "true", "resize-method": "display-update",
        "enable-wallpaper": "false", "color-depth": "24",
    }
    p = "\n".join(f"      <param name={quoteattr(k)}>{escape(v)}</param>" for k, v in params.items())
    return f'    <connection name="Kali-{n:02d}">\n      <protocol>rdp</protocol>\n{p}\n    </connection>'


def user(name, password, conns):
    h = hashlib.sha256(password.encode()).hexdigest()
    return f'  <authorize username={quoteattr(name)} password="{h}" encoding="sha256">\n' + "\n".join(conns) + "\n  </authorize>"


admin = next(r for r in rows if r["user"] == "admin")
xml = ["<user-mapping>"]
xml += [user(r["user"], r["password"], [connection(r)]) for r in participants]
xml.append(user("admin", admin["password"], [connection(r) for r in participants]))
xml.append("</user-mapping>")
os.makedirs(out_dir, exist_ok=True)
with open(f"{out_dir}/user-mapping.xml", "w") as f:
    f.write("\n".join(xml) + "\n")
os.chmod(f"{out_dir}/user-mapping.xml", 0o640)
print(f"{len(participants)} participants + admin -> {out_dir}/user-mapping.xml")
