# cam01.acme.lab - IP camera: web login page and an RTSP port that answers 401
DEBIAN_FRONTEND=noninteractive apt-get -y -qq install nginx socat >/dev/null
cat > /var/www/html/index.html <<'E'
<!doctype html><html><head><meta charset="utf-8"><title>ACME Cam 200 - Login</title></head>
<body style="font-family:sans-serif;background:#222;color:#eee;text-align:center;padding-top:5rem">
<h1>ACME Cam 200</h1><p>Firmware 1.0.4 (2019)</p>
<form method="post"><input name="user" placeholder="admin"><br><input name="pass" type="password"><br>
<button>Login</button></form><p><small>Default: admin / 12345</small></p></body></html>
E
sed -i 's/server_name _;/server_name _;\n\tserver_tokens on;/' /etc/nginx/sites-available/default
cat > /etc/systemd/system/fake-rtsp.service <<'E'
[Unit]
Description=Fake RTSP endpoint
[Service]
ExecStart=/usr/bin/socat TCP-LISTEN:554,fork,reuseaddr SYSTEM:'printf "RTSP/1.0 401 Unauthorized\\r\\nServer: ACME Cam RTSP 1.0\\r\\nWWW-Authenticate: Basic realm=\\"ACME Cam\\"\\r\\n\\r\\n"'
Restart=always
[Install]
WantedBy=multi-user.target
E
systemctl daemon-reload; systemctl enable --now fake-rtsp; systemctl restart nginx
