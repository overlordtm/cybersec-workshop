# vpn.acme.lab - "remote access" box with an old OpenSSH; shares the password from www's backup file
docker pull -q debian:stretch-slim >/dev/null  # via the daemon proxy; BuildKit itself ignores it
docker build -q --build-arg http_proxy=$PROXY -t acme/old-ssh /opt/acme >/dev/null
docker rm -f vpn 2>/dev/null || true
docker run -d --name vpn --restart unless-stopped --network host acme/old-ssh
