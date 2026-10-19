#!/usr/bin/env python3
"""Switch the lab scenario on both firewalls. Run on the PVE host.

Usage: scenario.py internet   participants are on the internet: only ACME's public IPs (default)
       scenario.py visitor    participants are plugged into ACME's office LAN (segmented ACME)
       scenario.py flat       participants are inside ACME and nothing is segmented
       scenario.py status

Rules whose description starts with "SCENARIO <modes>:" belong to those modes, e.g.
"SCENARIO visitor+flat: LAB to ACME internal" is on in visitor and flat. See the README.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from opnapi import Opn  # noqa: E402

MODES = ("internet", "visitor", "flat")
firewalls = [Opn("lab-gw"), Opn("acme-fw")]


def scenario_rules(api):
    return [r for r in api.rows("/api/firewall/filter/searchRule")
            if r.get("description", "").startswith("SCENARIO ")]


def modes_of(rule):
    return rule["description"].split()[1].rstrip(":").split("+")


if sys.argv[1:2] and sys.argv[1] in MODES:
    mode = sys.argv[1]
    for api in firewalls:
        for r in scenario_rules(api):
            want = "1" if mode in modes_of(r) else "0"
            if r["enabled"] != want:
                api.call(f"/api/firewall/filter/toggleRule/{r['uuid']}/{want}", {})
        # Existing connections (e.g. an open SMB session) survive until they close; new
        # connections and scans see the new rules at once. Not flushing states keeps
        # everyone's Guacamole session alive.
        api.call("/api/firewall/filter/apply", {})
elif sys.argv[1:] != ["status"]:
    sys.exit(__doc__)

rules = [(api, r) for api in firewalls for r in scenario_rules(api)]
for api, r in rules:
    print(f"{api.name:8} {'ON ' if r['enabled'] == '1' else 'off'}  {r['description']}")
current = [m for m in MODES if all((r["enabled"] == "1") == (m in modes_of(r)) for _, r in rules)]
print(f"\nscenario: {current[0] if current else 'mixed (rules switched by hand)'}")
