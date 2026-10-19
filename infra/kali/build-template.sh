#!/bin/sh
# Build the Kali template from Kali's official QEMU image. Run on the PVE host.
# Usage: build-template.sh [VMID]      (default 100; needs LAB-GW running for the proxy)
# Steps: download + verify image, create VM on the lab network, upgrade and install the
# workshop packages through the guest agent, run prepare-template.sh, convert to template.
set -eu
VMID=${1:-100}
HERE=$(cd "$(dirname "$0")" && pwd)
BASE=https://cdimage.kali.org/current
CACHE=/var/lib/vz/template/kali
PROXY=http://10.20.0.1:3128
PACKAGES="xrdp cloud-init cloud-guest-utils zaproxy cyberchef enum4linux-ng bind9-dnsutils nmap curl smbclient libimage-exiftool-perl wireshark snmp ffuf nikto sqlmap"

if qm status "$VMID" >/dev/null 2>&1; then echo "VM $VMID exists; delete it first" >&2; exit 1; fi

mkdir -p "$CACHE"; cd "$CACHE"
curl -sSfLO "$BASE/SHA256SUMS"
IMG=$(grep -oE 'kali-linux-[0-9.]+-qemu-amd64\.7z$' SHA256SUMS | head -1)
[ -f "$IMG" ] || { curl -sSfL -o "$IMG.part" "$BASE/$IMG" && mv "$IMG.part" "$IMG"; }
grep " $IMG\$" SHA256SUMS | sha256sum -c --quiet
QCOW=${IMG%.7z}.qcow2
if [ ! -f "$QCOW" ]; then  # extract to a temp dir first, so an interrupted run leaves nothing half-done
    rm -rf extract.tmp; 7z x -y -oextract.tmp "$IMG" >/dev/null
    mv extract.tmp/*.qcow2 "$QCOW"; rm -rf extract.tmp
fi
echo "image: $QCOW"

qm create "$VMID" --name kali-tmpl --ostype l26 --cores 4 --memory 4096 --cpu x86-64-v2-AES \
    --scsihw virtio-scsi-single --agent 1 --net0 virtio,bridge=lab,firewall=0 --tags "kali;lab;template"
qm importdisk "$VMID" "$QCOW" local-zfs >/dev/null
qm set "$VMID" --scsi0 "local-zfs:vm-$VMID-disk-0,iothread=1,discard=on" --boot order=scsi0 >/dev/null
qm start "$VMID"

gexec() { qm guest exec "$VMID" --timeout 60 -- sh -c "$1" 2>/dev/null; }
wait_agent() {
    t=0; until qm agent "$VMID" ping >/dev/null 2>&1; do
        sleep 5; t=$((t + 5)); [ $t -lt "${1:-600}" ] || { echo "no guest agent in VM $VMID" >&2; exit 1; }
    done
}
wait_agent 600

# Packages go through Squid on LAB-GW (the lab has no direct internet). The job runs as a
# systemd unit so that upgrading qemu-guest-agent does not kill it.
gexec "echo 'Acquire::http::Proxy \"$PROXY\";' > /etc/apt/apt.conf.d/95lab-proxy
       sed -i 's#http://http.kali.org/kali/#http://kali.download/kali/#' /etc/apt/sources.list.d/kali.sources"
gexec "systemd-run --unit=kali-build --setenv=DEBIAN_FRONTEND=noninteractive sh -c \
  '(apt-get update && apt-get -y -o Dpkg::Options::=--force-confold full-upgrade && \
    apt-get -y -o Dpkg::Options::=--force-confold install $PACKAGES; echo BUILD-EXIT=\$?) > /root/build.log 2>&1'" >/dev/null
t=0
while :; do
    sleep 30; t=$((t + 30))
    out=$(gexec "grep -o 'BUILD-EXIT=[0-9]*' /root/build.log" || true)
    case "$out" in *BUILD-EXIT=0*) break ;; *BUILD-EXIT=*) echo "package install failed" >&2; gexec "tail -20 /root/build.log"; exit 1 ;; esac
    [ $t -lt 7200 ] || { echo "package install timed out" >&2; exit 1; }
    qm agent "$VMID" ping >/dev/null 2>&1 || wait_agent 300
done
echo "packages installed"

qm guest exec "$VMID" --pass-stdin 1 --timeout 300 -- sh -c 'cat > /root/prepare.sh && sh /root/prepare.sh && rm -f /root/prepare.sh /root/build.log' \
    < "$HERE/prepare-template.sh" | grep -q PREPARE-OK
qm shutdown "$VMID" --timeout 180
qm set "$VMID" --net0 virtio,bridge=lab,firewall=1 --memory 3072 --cores 2 >/dev/null
qm template "$VMID"
echo "template $VMID ready"
