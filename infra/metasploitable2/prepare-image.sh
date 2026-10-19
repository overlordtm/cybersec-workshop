#!/bin/sh
# Run on PVE before OpenTofu. Customize an offline copy; never boot the upstream disk.
set -eu
DEST=/var/lib/vz/import/metasploitable2-acme.qcow2
[ ! -s "$DEST" ] || exit 0
mkdir -p /var/lib/vz/import
work=$(mktemp -d /var/lib/vz/import/.metasploitable2.XXXXXX)
trap 'rm -rf "$work"' EXIT HUP INT TERM
curl --fail --location --retry 3 \
    https://downloads.sourceforge.net/project/metasploitable/Metasploitable2/metasploitable-linux-2.0.0.zip \
    -o "$work/image.zip"
unzip -q "$work/image.zip" 'Metasploitable2-Linux/Metasploitable.vmdk' -d "$work"
qemu-img convert -f vmdk -O qcow2 "$work/Metasploitable2-Linux/Metasploitable.vmdk" "$work/disk.qcow2"
# Ubuntu 8.04 has neither cloud-init nor a modern guest agent. Remove VMware's
# MAC mapping so the single emulated NIC becomes eth0, and write ifupdown config.
cat > "$work/interfaces" <<'NET'
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 172.20.20.30
    netmask 255.255.255.0
    gateway 172.20.20.1
NET
LIBGUESTFS_BACKEND=direct virt-customize --no-network -a "$work/disk.qcow2" \
    --delete /etc/udev/rules.d/70-persistent-net.rules \
    --upload "$work/interfaces:/etc/network/interfaces" \
    --write '/etc/resolv.conf:nameserver 172.20.20.1
' \
    --write '/etc/hostname:metasploitable2
' \
    --write '/etc/hosts:127.0.0.1 localhost
127.0.1.1 metasploitable2.acme.lab metasploitable2
'
mv "$work/disk.qcow2" "$DEST"
echo PREPARED
