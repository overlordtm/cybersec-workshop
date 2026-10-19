#!/bin/sh
# Inject a bootstrap config.xml into a fresh OPNsense nano VM (created stopped by OpenTofu).
# Run on the PVE host:  bootstrap-vm.sh VMID CONFIG.xml [SSH-NAME]
# Attaches a small FAT disk with conf/config.xml, logs in on the serial console with the
# factory password, copies the config, reboots and removes the disk again.
set -eu
VMID=$1; CONFIG=$2; SSHNAME=${3:-}
F=/root/serial/$VMID.in; L=/root/serial/$VMID.log
VOL=local-zfs:vm-$VMID-disk-9

cleanup_disk() {
    qm set "$VMID" --delete scsi1 >/dev/null 2>&1 || true
    pvesm free "$VOL" >/dev/null 2>&1 || true
}

qm stop "$VMID" >/dev/null 2>&1 || true
cleanup_disk
pvesm alloc local-zfs "$VMID" "vm-$VMID-disk-9" 32M >/dev/null
udevadm settle
DEV=$(pvesm path "$VOL")
mkfs.vfat -n CONF "$DEV" >/dev/null
M=$(mktemp -d); mount "$DEV" "$M"; mkdir "$M/conf"; cp "$CONFIG" "$M/conf/config.xml"; umount "$M"; rmdir "$M"
qm set "$VMID" --scsi1 "$VOL" >/dev/null

mkdir -p /root/serial; : > "$L"
qm start "$VMID"
systemctl stop "serial-$VMID" 2>/dev/null || true
systemctl reset-failed "serial-$VMID" 2>/dev/null || true
systemd-run --unit="serial-$VMID" /usr/local/bin/serial-relay "$VMID" >/dev/null

wait_for() { # regex timeout
    t=0
    until tr -d '\r' < "$L" | grep -qE "$1"; do
        sleep 3; t=$((t + 3))
        [ $t -lt "$2" ] || { echo "timeout waiting for '$1' on VM $VMID" >&2; exit 1; }
    done
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
cleanup_disk
# A rebuilt box has new SSH host keys
[ -z "$SSHNAME" ] || ssh-keygen -R "$(ssh -G "$SSHNAME" | awk '/^hostname /{print $2}')" -f /root/.ssh/known_hosts_lab >/dev/null 2>&1 || true
tr -d '\r' < "$L" | sed 's/\x1b\[[0-9;]*[a-zA-Z]//g' | grep -A8 '^\*\*\* '
