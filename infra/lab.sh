#!/bin/sh
# Workshop lab: set up, tear down, reset. Run from your laptop in infra/.
#
#   ./lab.sh up [KALI] [WG] build/update (default 15 hosted Kali, 0 WireGuard participants)
#   ./lab.sh down          destroy everything OpenTofu created (keeps host layer + Kali template)
#   ./lab.sh down --all    ... and also the Kali template, vmbr1/NAT, firewall lines, API token
#   ./lab.sh reset         roll firewalls/Guacamole/ACME back to "clean", recreate Kali clones
#   ./lab.sh kalis         recreate Kali clones only (fresh desktops)
#   ./lab.sh start|stop [N ...]   start/stop Kali clones (all, or by number)
#   ./lab.sh scenario internet|visitor|flat|status   switch what participants can reach
#   ./lab.sh credentials   export encrypted credentials for the exercise site
#   ./lab.sh claim-pdf     print active claim codes as cut-out A4 slips
#   ./lab.sh status        what exists and what is running
set -eu
cd "$(dirname "$0")"
PVE=root@pve.digilab-g.rtfm.si
COUNT_FILE=secrets/kali-count
WG_COUNT_FILE=secrets/wg-count

count() { cat "$COUNT_FILE" 2>/dev/null || echo 15; }
wg_count() { cat "$WG_COUNT_FILE" 2>/dev/null || echo 0; }
play() { (cd ansible && ansible-playbook "$@"); }
tofu_() {
    TF_VAR_pve_api_token=$(cat secrets/pve-token) tofu -chdir=tofu "$@"
}
template_exists() { ssh -o BatchMode=yes $PVE "qm status 100" >/dev/null 2>&1; }
kali_ids() {
    if [ $# -gt 0 ]; then for n in "$@"; do echo $((200 + n)); done
    else seq 201 $((200 + $(count))); fi
}

cmd=${1:-help}; shift || true
case $cmd in
up)
    [ $# -le 2 ] || { echo "Usage: ./lab.sh up [KALI_COUNT] [WG_COUNT]" >&2; exit 1; }
    N=${1:-$(count)}
    W=${2:-$(wg_count)}
    mkdir -p -m 700 secrets
    python3 -I guacamole/gen-users.py secrets secrets/guacamole-home "$N" "$W"
    echo "$N" > "$COUNT_FILE"
    echo "$W" > "$WG_COUNT_FILE"
    play host.yml
    tofu_ init -input=false >/dev/null
    if template_exists; then K=$N; else K=0; fi
    tofu_ apply -input=false -auto-approve -var kali_count="$K"
    play site.yml -e kali_count="$N" -e wg_count="$W"
    if [ "$N" -gt 0 ] && [ "$K" = 0 ]; then
        play kali-template.yml
        tofu_ apply -input=false -auto-approve -var kali_count="$N"
    fi
    echo "Lab is up: https://lab.digilab-g.rtfm.si/  (Kali clones are stopped: ./lab.sh start)"
    ;;
down)
    tofu_ destroy -input=false -auto-approve -var kali_count="$(count)"
    if [ "${1:-}" = --all ]; then play teardown-host.yml; fi
    ;;
reset)
    play reset.yml
    play site.yml -e kali_count="$(count)" -e wg_count="$(wg_count)"
    "$0" kalis
    ;;
kalis)
    replace=""
    for id in $(kali_ids); do replace="$replace -replace=proxmox_virtual_environment_vm.kali[\"kali-$(printf %02d $((id - 200)))\"]"; done
    # shellcheck disable=SC2086
    tofu_ apply -input=false -auto-approve -var kali_count="$(count)" $replace
    ;;
start|stop)
    for id in $(kali_ids "$@"); do ssh -o BatchMode=yes $PVE "qm $cmd $id" && echo "$cmd $id"; done
    ;;
scenario)
    ssh -o BatchMode=yes $PVE "python3 -I /root/lab/opnsense/scenario.py ${1:-status}"
    ;;
credentials)
    "${CREDENTIALS_PYTHON:-python3}" -I export-credentials.py "$@"
    ;;
claim-pdf)
    "${CREDENTIALS_PYTHON:-python3}" -I print-claim-codes.py "$@"
    ;;
status)
    tofu_ output
    ssh -o BatchMode=yes $PVE 'qm list | grep -E "VMID|kali|gw|fw|greenbone"; pct list' 2>/dev/null
    ;;
*)
    sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
    ;;
esac
