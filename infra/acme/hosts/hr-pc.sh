# hr-pc.acme.lab - HR workstation sharing its documents folder (SMB) on the office network
DEBIAN_FRONTEND=noninteractive apt-get -y -qq install samba >/dev/null
mkdir -p /srv/dokumenti && printf 'Pogodba o zaposlitvi - predloga\n' > /srv/dokumenti/pogodba-predloga.txt
chmod -R a+rX /srv/dokumenti
cat > /etc/samba/smb.conf <<'E'
[global]
   workgroup = ACME
   server string = HR-PC
   netbios name = HR-PC
   map to guest = Bad User
[Dokumenti]
   path = /srv/dokumenti
   guest ok = yes
   read only = yes
E
systemctl restart smbd nmbd
