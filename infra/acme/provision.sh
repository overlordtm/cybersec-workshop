#!/bin/sh
# Install and configure ACME servers inside their LXC containers (created by OpenTofu).
# Run on the PVE host from this directory.
# Usage: provision.sh [name ...]      (default: all hosts in hosts.csv)
#   Hosts already provisioned are skipped; FORCE=1 provisions again.
set -eu
cd "$(dirname "$0")"
PROXY=http://198.51.100.1:3128

tail -n +2 hosts.csv | while IFS=, read -r id name seg ip mem docker; do
    [ $# -eq 0 ] || echo " $* " | grep -q " $name " || continue
    if [ "${FORCE:-0}" != 1 ] && pct exec "$id" -- test -f /root/.acme-provisioned; then
        echo "$name ($id): already provisioned"; continue
    fi
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
    if [ -d "files/$name" ]; then
        tar -C "files/$name" -cf - . | pct exec "$id" -- sh -c 'mkdir -p /opt/acme && tar -C /opt/acme -xf -'
    fi
    pct push "$id" "hosts/$name.sh" /root/setup.sh
    pct exec "$id" -- env PROXY=$PROXY sh -e /root/setup.sh
    pct exec "$id" -- touch /root/.acme-provisioned
    echo "$name ($id, $ip): provisioned"
done
