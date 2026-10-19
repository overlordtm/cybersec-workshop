#!/bin/sh
# Create (or recreate) Kali clones from template 100. Run on the PVE host.
# Usage: clones.sh FIRST LAST [participants.csv]     e.g. clones.sh 1 15 /root/lab/participants.csv
#   VMID 200+N, name kali-NN, MAC bc:24:11:20:00:NN (DHCP reservation 10.20.0.(100+N) on LAB-GW),
#   user "kali" with the participant's password (same as their Guacamole login).
set -eu
FIRST=$1; LAST=$2; CSV=${3:-/root/lab/participants.csv}
TEMPLATE=100

# Security group: Kalis accept RDP from Guacamole only and cannot talk to each other.
FW=/etc/pve/firewall/cluster.fw
if ! grep -q '^\[group kali\]' $FW; then
    cat >> $FW <<'G'

[group kali] # Kali workstations: no Kali-to-Kali traffic

IN ACCEPT -source 10.20.0.10 -p tcp -dport 3389 -log nolog # RDP from Guacamole
IN ACCEPT -source 10.20.0.1 -p icmp -log nolog # ping from LAB-GW
OUT ACCEPT -dest 10.20.0.1 -log nolog # gateway: DNS, proxy, routing to ACME
OUT DROP -dest 10.20.0.0/24 -log nolog # no other lab hosts
G
fi

for n in $(seq "$FIRST" "$LAST"); do
    id=$((200 + n)); nn=$(printf %02d "$n"); name=kali-$nn
    pw=$(awk -F, -v u="udelezenec$nn" '$2==u {print $3}' "$CSV")
    [ -n "$pw" ] || { echo "no password for $name in $CSV" >&2; exit 1; }
    if qm status $id >/dev/null 2>&1; then
        qm stop $id --skiplock 1 >/dev/null 2>&1 || true
        qm destroy $id --purge 1 >/dev/null
    fi
    qm clone $TEMPLATE $id --name $name >/dev/null
    qm set $id --net0 virtio=BC:24:11:20:00:$nn,bridge=lab,firewall=1 \
        --ide2 local-zfs:cloudinit --ciuser kali --cipassword "$pw" --ipconfig0 ip=dhcp \
        --tags "lab;kali" --onboot 0 >/dev/null
    cat > /etc/pve/firewall/$id.fw <<V
[OPTIONS]

enable: 1
policy_in: DROP
policy_out: ACCEPT
dhcp: 1
macfilter: 1

[RULES]

GROUP kali
V
    echo "$name: VMID $id, 10.20.0.$((100 + n))"
done
