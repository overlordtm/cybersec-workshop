#!/bin/sh
# Prepare kali-tmpl for cloning. Run inside the VM as root (qm guest exec).
# Assumes workshop packages from build-template.sh are installed.
set -eu

PROXY=http://10.20.0.1:3128
NO_PROXY=localhost,127.0.0.1,10.20.0.0/16,172.20.0.0/16,198.51.100.0/24,.acme.lab,.lab.internal

# --- Proxy (the lab has no direct internet; Squid allows an allowlist only)
sed -i '/^\(http\|https\|no\)_proxy=/Id' /etc/environment
cat >> /etc/environment <<E
http_proxy=$PROXY
https_proxy=$PROXY
no_proxy=$NO_PROXY
HTTP_PROXY=$PROXY
HTTPS_PROXY=$PROXY
NO_PROXY=$NO_PROXY
E
echo "Acquire::http::Proxy \"$PROXY\";" > /etc/apt/apt.conf.d/95lab-proxy
sed -i 's#http://http.kali.org/kali/#http://kali.download/kali/#' /etc/apt/sources.list.d/kali.sources

mkdir -p /usr/lib/firefox-esr/distribution
cat > /usr/lib/firefox-esr/distribution/policies.json <<E
{"policies": {
  "Proxy": {"Mode": "manual", "HTTPProxy": "10.20.0.1:3128", "UseHTTPProxyForAllProtocols": true,
            "Passthrough": "localhost, 127.0.0.1, 10.20.0.0/16, 172.20.0.0/16, 198.51.100.0/24, .acme.lab",
            "Locked": false},
  "DisableTelemetry": true, "DisableFirefoxStudies": true, "DontCheckDefaultBrowser": true,
  "OverrideFirstRunPage": "", "NoDefaultBookmarks": false
}}
E

# --- xrdp with XFCE
adduser xrdp ssl-cert >/dev/null 2>&1 || true
systemctl enable xrdp xrdp-sesman >/dev/null 2>&1
# Silence colord/packagekit authentication prompts in remote sessions
mkdir -p /etc/polkit-1/rules.d
cat > /etc/polkit-1/rules.d/45-xrdp-colord.rules <<'E'
polkit.addRule(function(action, subject) {
  if ((action.id.indexOf("org.freedesktop.color-manager.") == 0 ||
       action.id.indexOf("org.freedesktop.packagekit.") == 0) && subject.isInGroup("users")) {
    return polkit.Result.YES;
  }
});
E
usermod -aG users kali

# --- cloud-init: hostname, password, identity only. Network stays with NetworkManager (DHCP
# reservations on LAB-GW give every clone its IP).
cat > /etc/cloud/cloud.cfg.d/99-lab.cfg <<'E'
datasource_list: [NoCloud, ConfigDrive, None]
network: {config: disabled}
preserve_hostname: false
manage_etc_hosts: true
ssh_pwauth: false
E
systemctl enable cloud-init-local cloud-init cloud-config cloud-final >/dev/null 2>&1 || true

# Undo the temporary DNS override used during setup
for c in $(nmcli -g UUID con show); do
  nmcli con mod "$c" ipv4.dns "" ipv4.ignore-auto-dns no 2>/dev/null || true
done

# --- Clean up so every clone is unique and the template is small
apt-get -y autoremove >/dev/null; apt-get clean
rm -f /root/apt.log /root/.bash_history /home/kali/.bash_history /home/kali/.zsh_history /root/.zsh_history
rm -rf /tmp/* /var/tmp/* /home/kali/.cache/* /var/lib/NetworkManager/*.lease /var/lib/dhcp/*
journalctl --rotate >/dev/null 2>&1; journalctl --vacuum-time=1s >/dev/null 2>&1 || true
rm -f /etc/ssh/ssh_host_*
truncate -s 0 /etc/machine-id; rm -f /var/lib/dbus/machine-id
cloud-init clean --logs >/dev/null 2>&1 || true
fstrim -av >/dev/null 2>&1 || true
echo PREPARE-OK
