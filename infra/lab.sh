#!/bin/sh
# Workshop lab: set up, tear down, reset. Run from your laptop in infra/.
#
#   ./lab.sh up [N]        build or update everything (N Kali workstations, default 15)
#   ./lab.sh down          destroy everything OpenTofu created (keeps host layer + Kali template)
#   ./lab.sh down --all    ... and also the Kali template, vmbr1/NAT, firewall lines, API token
#   ./lab.sh reset         roll firewalls/Guacamole/ACME back to "clean", recreate Kali clones
#   ./lab.sh kalis         recreate Kali clones only (fresh desktops)
#   ./lab.sh start|stop [N ...]   start/stop Kali clones (all, or by number)
#   ./lab.sh status        what exists and what is running
set -eu
cd "$(dirname "$0")"
PVE=root@pve.digilab-g.rtfm.si
COUNT_FILE=secrets/kali-count

count() { cat "$COUNT_FILE" 2>/dev/null || echo 15; }
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
    [ $# -gt 0 ] && echo "$1" > "$COUNT_FILE"
    N=$(count)
    mkdir -p -m 700 secrets
    python3 -I guacamole/gen-users.py secrets secrets/guacamole-home "$N"
    play host.yml
    tofu_ init -input=false >/dev/null
    if template_exists; then K=$N; else K=0; fi
    tofu_ apply -input=false -auto-approve -var kali_count="$K"
    play site.yml -e kali_count="$N"
    if [ "$K" = 0 ]; then
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
status)
    tofu_ output
    ssh -o BatchMode=yes $PVE 'qm list | grep -E "VMID|kali|gw|fw"; pct list' 2>/dev/null
    ;;
*)
    sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
    ;;
esac
