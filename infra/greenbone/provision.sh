#!/bin/sh
# Runs INSIDE VM 112. Read the managed admin password from stdin, never the CLI.
set -eu
umask 077
IFS= read -r ADMIN_PASSWORD
[ -n "$ADMIN_PASSWORD" ]
cd /opt/greenbone
# cloud-init returns 2 for recoverable warnings too (including Proxmox's
# deprecated string-form `user` field). Only a fatal error should stop setup.
cloud_init_rc=0
cloud-init status --wait --long || cloud_init_rc=$?
case "$cloud_init_rc" in
    0) ;;
    2) echo 'cloud-init completed with recoverable warnings; continuing.' ;;
    *) echo "cloud-init failed (exit $cloud_init_rc)" >&2; exit "$cloud_init_rc" ;;
esac
echo 'Acquire::http::Proxy "http://10.20.0.1:3128";' > /etc/apt/apt.conf.d/95proxy
if ! command -v docker >/dev/null || ! docker compose version >/dev/null 2>&1; then
    apt-get -qq update
    DEBIAN_FRONTEND=noninteractive apt-get -y -qq install docker.io docker-compose ca-certificates
fi
mkdir -p /etc/systemd/system/docker.service.d
cat > /etc/systemd/system/docker.service.d/proxy.conf <<'EOF'
[Service]
Environment="HTTP_PROXY=http://10.20.0.1:3128" "HTTPS_PROXY=http://10.20.0.1:3128" "NO_PROXY=localhost,127.0.0.1,::1"
EOF
systemctl daemon-reload
systemctl enable --now docker
# Load proxy configuration without interrupting a running scanner on each lab.sh up.
# systemctl show reflects the reloaded unit even when the running daemon still
# has its old environment (Docker starts during apt install). Query Docker itself.
if [ "$(docker info --format '{{.HTTPProxy}} {{.HTTPSProxy}}')" != \
    'http://10.20.0.1:3128 http://10.20.0.1:3128' ]; then
    systemctl restart docker
fi
docker compose config --quiet
# Keep nginx stopped until the upstream default admin password has been replaced.
docker compose stop nginx
# First install downloads feeds too. Later runs retain the images; update explicitly
# with `docker compose pull && docker compose up -d` during maintenance.
set -f
set -- $(docker compose config --services | sed '/^nginx$/d; /^gvm-tools$/d')
docker compose up -d --pull missing --quiet-pull "$@"
# Wait for the manager socket so the CLI cannot race initial database migrations.
attempt=0
until docker compose exec -T gvmd test -S /run/gvmd/gvmd.sock && \
    printf '%s\n' "$ADMIN_PASSWORD" | docker compose exec -T -u gvmd gvmd sh -c \
    'IFS= read -r password; gvmd --user=admin --new-password="$password"'; do
    attempt=$((attempt + 1))
    [ "$attempt" -lt 360 ] || { echo 'gvmd administrator setup timed out' >&2; exit 1; }
    sleep 10
done
unset ADMIN_PASSWORD
docker compose up -d --quiet-pull nginx
echo 'Greenbone started. Wait for Administration > Feed Status before scanning.'
