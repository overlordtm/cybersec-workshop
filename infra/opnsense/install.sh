#!/bin/sh
# Install an OPNsense VM from the nano image with a prepared bootstrap config.xml.
# Run on the PVE host. Usage:
#   install.sh VMID NAME CONFIG.xml BRIDGE [BRIDGE...]     (net0 = first bridge = WAN in the profile)
# Needs /usr/local/bin/serial-relay (infra/host/serial-relay.py).
set -eu
VMID=$1; NAME=$2; CONFIG=$3; shift 3
IMG=/var/lib/vz/template/opnsense/OPNsense-26.7-nano-amd64.img
F=/root/serial/$VMID.in; L=/root/serial/$VMID.log

nets=""; i=0
for br in "$@"; do nets="$nets --net$i virtio,bridge=$br,firewall=0"; i=$((i + 1)); done

qm create "$VMID" --name "$NAME" --ostype other --cores 2 --memory 2048 --balloon 0 --cpu x86-64-v2-AES \
    --scsihw virtio-scsi-single --serial0 socket --vga serial0 --onboot 1 --startup order=1 \
    --tags "lab;router" $nets
qm importdisk "$VMID" "$IMG" local-zfs >/dev/null
qm set "$VMID" --scsi0 "local-zfs:vm-$VMID-disk-0,iothread=1,discard=on" --boot order=scsi0 >/dev/null
qm resize "$VMID" scsi0 16G

# Config disk: FAT image with conf/config.xml
pvesm alloc local-zfs "$VMID" "vm-$VMID-disk-9" 32M >/dev/null
CIMG=$(pvesm path "local-zfs:vm-$VMID-disk-9")
udevadm settle
mkfs.vfat -n CONF "$CIMG" >/dev/null
M=$(mktemp -d); mount -o loop "$CIMG" "$M"; mkdir "$M/conf"; cp "$CONFIG" "$M/conf/config.xml"; umount "$M"; rmdir "$M"
qm set "$VMID" --scsi1 "local-zfs:vm-$VMID-disk-9" >/dev/null

mkdir -p /root/serial; : > "$L"
qm start "$VMID"
systemctl stop "serial-$VMID" 2>/dev/null || true
systemctl reset-failed "serial-$VMID" 2>/dev/null || true
systemd-run --unit="serial-$VMID" /usr/local/bin/serial-relay "$VMID" >/dev/null

wait_for() { # regex timeout
    t=0; until tr -d '\r' < "$L" | grep -qE "$1"; do sleep 3; t=$((t + 3)); [ $t -lt "$2" ] || { echo "timeout waiting for $1" >&2; exit 1; }; done
}
send() { printf '%s\r' "$1" > "$F"; sleep "${2:-2}"; }

wait_for 'login: *$' 600
send root; send opnsense 4; send 8 3
: > "$L"
send "mount_msdosfs /dev/da1 /mnt && cp /mnt/conf/config.xml /conf/config.xml && umount /mnt && echo CONF-OK" 4
wait_for '^CONF-OK' 30
: > "$L"
send reboot 5
wait_for 'login: *$' 600
qm set "$VMID" --delete scsi1 >/dev/null
qm disk unlink "$VMID" --idlist unused0 --force 1 >/dev/null 2>&1 || pvesm free "local-zfs:vm-$VMID-disk-9" >/dev/null
tr -d '\r' < "$L" | sed 's/\x1b\[[0-9;]*[a-zA-Z]//g' | grep -A6 '^\*\*\* '
