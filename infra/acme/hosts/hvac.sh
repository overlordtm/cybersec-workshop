# hvac.acme.lab - building controller: Modbus/TCP (502) without authentication and a web panel
DEBIAN_FRONTEND=noninteractive apt-get -y -qq install python3-pymodbus nginx >/dev/null
cat > /usr/local/bin/hvac-modbus.py <<'E'
#!/usr/bin/env python3
# Holding registers: 0 = set temperature (x10), 1 = measured temperature (x10), 2 = fan on/off
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext
try:
    from pymodbus.datastore import ModbusDeviceContext as Ctx
except ImportError:
    from pymodbus.datastore import ModbusSlaveContext as Ctx
store = Ctx(hr=ModbusSequentialDataBlock(0, [215, 223, 1] + [0] * 97))
try:
    context = ModbusServerContext(devices=store, single=True)
except TypeError:
    context = ModbusServerContext(slaves=store, single=True)
StartTcpServer(context=context, address=("0.0.0.0", 502))
E
chmod +x /usr/local/bin/hvac-modbus.py
cat > /etc/systemd/system/hvac-modbus.service <<'E'
[Unit]
Description=HVAC Modbus/TCP simulator
[Service]
ExecStart=/usr/local/bin/hvac-modbus.py
Restart=always
AmbientCapabilities=CAP_NET_BIND_SERVICE
[Install]
WantedBy=multi-user.target
E
printf '<!doctype html><meta charset="utf-8"><title>ACME HVAC</title><h1>Klimatska naprava - streha</h1><p>Nastavljena temperatura: 21,5 &deg;C</p><p>Upravlja: zunanji serviser (Modbus/TCP 502)</p>\n' > /var/www/html/index.html
systemctl daemon-reload; systemctl enable --now hvac-modbus; systemctl restart nginx
