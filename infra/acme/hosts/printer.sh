# printer.acme.lab - network printer: raw printing (9100), SNMP with community "public", status page
DEBIAN_FRONTEND=noninteractive apt-get -y -qq install snmpd socat nginx >/dev/null
cat > /etc/snmp/snmpd.conf <<'E'
agentAddress udp:161
rocommunity public
sysDescr ACME LaserPrint 4000, firmware 2.1.0 (2018)
sysLocation 1. nadstropje, pisarna 12
sysContact peter.horvat@acme.lab
sysName printer.acme.lab
E
cat > /etc/systemd/system/jetdirect.service <<'E'
[Unit]
Description=Raw printing port 9100
[Service]
ExecStart=/usr/bin/socat TCP-LISTEN:9100,fork,reuseaddr OPEN:/dev/null,wronly
Restart=always
[Install]
WantedBy=multi-user.target
E
printf '<!doctype html><meta charset="utf-8"><title>ACME LaserPrint 4000</title><h1>ACME LaserPrint 4000</h1><p>Stanje: pripravljen. Toner: 23%%</p>\n' > /var/www/html/index.html
systemctl daemon-reload; systemctl enable --now jetdirect; systemctl restart snmpd nginx
