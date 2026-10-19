#!/bin/sh
# Create ACME servers as LXC containers and provision them. Run on the PVE host from this directory.
# Usage: deploy.sh [name ...]      (default: all hosts in hosts.tsv; existing containers are recreated)
set -eu
cd "$(dirname "$0")"
TEMPLATE=local:vztmpl/debian-13-standard_13.6-1_amd64.tar.zst
PROXY=http://198.51.100.1:3128

grep -v '^#' hosts.tsv | while IFS="$(printf '\t')" read -r id name seg ip mem docker; do
    [ $# -eq 0 ] || echo " $* " | grep -q " $name " || continue
    gw=${ip%.*}.1
    if pct status "$id" >/dev/null 2>&1; then pct stop "$id" >/dev/null 2>&1 || true; pct destroy "$id" --purge 1 >/dev/null; fi
    features="--features nesting=1"; [ "$docker" = yes ] && features="--features nesting=1,keyctl=1"
    pct create "$id" $TEMPLATE --hostname "$name" --cores 1 --memory "$mem" --swap 256 --rootfs local-zfs:4 \
        --net0 "name=eth0,bridge=$seg,ip=$ip/24,gw=$gw" --nameserver "$gw" --searchdomain acme.lab \
        --unprivileged 1 $features --ssh-public-keys /root/.ssh/lab_ed25519.pub \
        --onboot 1 --startup order=3 --tags "acme;$seg" --timezone Europe/Ljubljana >/dev/null
    pct start "$id"; sleep 3
    pct exec "$id" -- sh -c "
        systemctl disable --now ssh ssh.socket >/dev/null 2>&1 || true
        echo 'Acquire::http::Proxy \"$PROXY\";' > /etc/apt/apt.conf.d/95proxy
        apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get -y -qq full-upgrade >/dev/null"
    if [ "$docker" = yes ]; then
        pct exec "$id" -- sh -c "
            DEBIAN_FRONTEND=noninteractive apt-get -y -qq install docker.io >/dev/null
            mkdir -p /etc/systemd/system/docker.service.d
            printf '[Service]\nEnvironment=HTTP_PROXY=$PROXY HTTPS_PROXY=$PROXY\n' > /etc/systemd/system/docker.service.d/proxy.conf
            systemctl daemon-reload; systemctl restart docker"
    fi
    # Host files (optional) and setup script
    if [ -d "files/$name" ]; then
        tar -C "files/$name" -cf - . | pct exec "$id" -- sh -c 'mkdir -p /opt/acme && tar -C /opt/acme -xf -'
    fi
    pct push "$id" "hosts/$name.sh" /root/setup.sh
    pct exec "$id" -- env PROXY=$PROXY sh -e /root/setup.sh
    echo "$name ($id, $ip): ok"
done
