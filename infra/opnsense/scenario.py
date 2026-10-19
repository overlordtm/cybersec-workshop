#!/usr/bin/env python3
"""Switch ACME-FW scenario rules live. Run on the PVE host.

Usage: scenario.py status
       scenario.py visitor on|off    lab and VPN reach ACME LAN (meeting room socket)
       scenario.py flat on|off       no segmentation at all
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from opnapi import Opn  # noqa: E402

api = Opn("acme-fw")
rules = [r for r in api.rows("/api/firewall/filter/searchRule") if r.get("description", "").startswith("SCENARIO")]

if len(sys.argv) == 3 and sys.argv[2] in ("on", "off"):
    want = "1" if sys.argv[2] == "on" else "0"
    for r in rules:
        if r["description"].split()[1] == sys.argv[1]:
            api.call(f"/api/firewall/filter/toggleRule/{r['uuid']}/{want}", {})
    api.call("/api/firewall/filter/apply", {})
    rules = [r for r in api.rows("/api/firewall/filter/searchRule") if r.get("description", "").startswith("SCENARIO")]
elif sys.argv[1:] != ["status"]:
    sys.exit(__doc__)

for r in rules:
    print(f"{'ON ' if r['enabled'] == '1' else 'off'}  {r['description']}")
