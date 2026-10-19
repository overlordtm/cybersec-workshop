#!/bin/sh
# Bring an OPNsense box up to date and install plugins. Run on the PVE host.
# Usage: firmware.sh NAME [plugin ...]        e.g. firmware.sh lab-gw os-squid os-caddy
# NAME is the /root/.config/opn and ~/.ssh/config name. Reboots the box if the update needs it.
set -eu
NAME=$1; shift

wait_api() {
    t=0; until opn "$NAME" GET /api/core/system/status 2>/dev/null | grep -q metadata; do
        sleep 10; t=$((t + 10)); [ $t -lt 900 ] || { echo "$NAME API not reachable" >&2; exit 1; }
    done
}
wait_job() {
    sleep 10
    until opn "$NAME" GET /api/core/firmware/upgradestatus 2>/dev/null | grep -qE '"status":"(done|reboot|error)"'; do sleep 10; done
    opn "$NAME" GET /api/core/firmware/upgradestatus | grep -o '"status":"[a-z]*"'
}

wait_api
opn "$NAME" POST /api/core/firmware/check >/dev/null; sleep 30
if opn "$NAME" GET /api/core/firmware/status | grep -qE '"(upgrade|new|reinstall)_packages":\[\{'; then
    opn "$NAME" POST /api/core/firmware/update >/dev/null
    if wait_job | grep -q reboot; then
        echo "$NAME: rebooting after update"; sleep 60; wait_api
    fi
fi
for p in "$@"; do
    if ssh "$NAME" pkg info -q "$p" >/dev/null 2>&1; then continue; fi
    opn "$NAME" POST "/api/core/firmware/install/$p" >/dev/null
    wait_job >/dev/null
    ssh "$NAME" pkg info -q "$p" >/dev/null || { echo "$NAME: failed to install $p" >&2; exit 1; }
    echo "$NAME: installed $p"
done
echo "$NAME: $(ssh "$NAME" opnsense-version)"
