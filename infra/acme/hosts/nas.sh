# nas.acme.lab - "backup NAS" web UI (File Browser 2.23) with default credentials admin/admin
mkdir -p /srv/backup/2026
printf 'varnostna kopija baze - oktober 2026\n' > /srv/backup/2026/baza-2026-10.sql
docker rm -f nas 2>/dev/null || true
docker run -d --name nas --restart unless-stopped -p 80:80 -v /srv/backup:/srv filebrowser/filebrowser:v2.23.0
