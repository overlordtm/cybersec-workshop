#!/usr/bin/env python3
"""Generate participant credentials and Guacamole's user-mapping.xml.

Usage: gen-users.py SECRETS_DIR OUT_DIR [COUNT]
Credentials are kept in SECRETS_DIR/participants.csv (created once, then reused):
  n,user,password   -- Guacamole login == Kali login (user "kali") password
"""
import csv, hashlib, os, secrets, sys
from xml.sax.saxutils import quoteattr

secrets_dir, out_dir = sys.argv[1:3]
count = int(sys.argv[3]) if len(sys.argv) > 3 else 15
path = f"{secrets_dir}/participants.csv"
words = "jabolko hruska sliva breskev marelica cesnja visnja jagoda malina robida".split()

rows = list(csv.DictReader(open(path))) if os.path.exists(path) else []
for n in range(len(rows) + 1, count + 1):
    pw = f"{secrets.choice(words)}-{secrets.randbelow(9000) + 1000}-{secrets.token_hex(2)}"
    rows.append({"n": str(n), "user": f"udelezenec{n:02d}", "password": pw})
rows.append({"n": "0", "user": "admin", "password": secrets.token_urlsafe(16)}) if not any(
    r["user"] == "admin" for r in rows) else None
with open(path, "w", newline="") as f:
    w = csv.DictWriter(f, ["n", "user", "password"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
os.chmod(path, 0o600)

participants = [r for r in rows if r["user"] != "admin" and int(r["n"]) <= count]


def connection(r):
    n = int(r["n"])
    params = {
        "hostname": f"10.20.0.{100 + n}", "port": "3389", "username": "kali", "password": r["password"],
        "security": "any", "ignore-cert": "true", "resize-method": "display-update",
        "enable-wallpaper": "false", "color-depth": "24",
    }
    p = "\n".join(f"      <param name={quoteattr(k)}>{v}</param>" for k, v in params.items())
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
