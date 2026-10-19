# intranet.acme.lab - internal portal over plain HTTP with Basic auth (credentials travel unencrypted)
DEBIAN_FRONTEND=noninteractive apt-get -y -qq install nginx apache2-utils >/dev/null
mkdir -p /var/www/intranet
cat > /var/www/intranet/index.html <<'E'
<!doctype html><html lang="sl"><head><meta charset="utf-8"><title>ACME intranet</title></head>
<body style="font-family:sans-serif;max-width:50rem;margin:2rem auto">
<h1>ACME intranet</h1><ul><li>Malica: ponedeljek – petek ob 10:00</li>
<li>Datoteke: \\files\javno</li><li>Varnostne kopije: http://nas.acme.lab/</li></ul></body></html>
E
htpasswd -bc /etc/nginx/intranet.htpasswd zaposleni acme123 >/dev/null
cat > /etc/nginx/sites-available/default <<'E'
server {
    listen 80 default_server;
    root /var/www/intranet;
    auth_basic "ACME intranet";
    auth_basic_user_file /etc/nginx/intranet.htpasswd;
}
E
systemctl restart nginx
