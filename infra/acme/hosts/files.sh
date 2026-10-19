# files.acme.lab - Samba file server. Share "javno" is readable without a password and contains
# documents whose metadata (author, software, dates) names employees (link to session 1).
DEBIAN_FRONTEND=noninteractive apt-get -y -qq install samba libimage-exiftool-perl >/dev/null
mkdir -p /srv/javno /srv/uprava
cp -r /opt/acme/javno/. /srv/javno/; cp -r /opt/acme/uprava/. /srv/uprava/
exiftool -q -overwrite_original -Author="Maja Kovac" -Creator="Maja Kovac" -Producer="LibreOffice 7.0" \
    -Title="Interni cenik 2026" /srv/javno/cenik-2026.pdf
chmod -R a+rX /srv/javno; chmod 700 /srv/uprava
cat > /etc/samba/smb.conf <<'E'
[global]
   workgroup = ACME
   server string = ACME datotecni streznik
   netbios name = FILES
   map to guest = Bad User
   server min protocol = NT1
   log level = 1
[javno]
   path = /srv/javno
   guest ok = yes
   read only = yes
   comment = Javni dokumenti
[uprava]
   path = /srv/uprava
   valid users = maja.kovac
   read only = no
   comment = Uprava - zaupno
E
id maja.kovac >/dev/null 2>&1 || useradd -M -s /usr/sbin/nologin maja.kovac
printf 'Maja2024\nMaja2024\n' | smbpasswd -s -a maja.kovac >/dev/null
systemctl restart smbd nmbd
