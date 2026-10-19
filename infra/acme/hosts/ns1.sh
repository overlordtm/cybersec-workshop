# ns1.acme.lab - authoritative DNS for acme.lab. Zone transfer (AXFR) is allowed to anyone:
# it reveals internal names and addresses (finding for session 2).
DEBIAN_FRONTEND=noninteractive apt-get -y -qq install bind9 >/dev/null
cat > /etc/bind/named.conf.options <<'E'
options {
    directory "/var/cache/bind";
    recursion no;
    allow-transfer { any; };
    listen-on { any; };
    listen-on-v6 { none; };
    version "BIND 9";
};
E
cat > /etc/bind/named.conf.local <<'E'
zone "acme.lab" { type master; file "/etc/bind/db.acme.lab"; };
E
cat > /etc/bind/db.acme.lab <<'E'
$TTL 3600
@        IN SOA ns1.acme.lab. hostmaster.acme.lab. ( 2026101902 3600 900 604800 3600 )
         IN NS  ns1.acme.lab.
         IN MX  10 mail.acme.lab.
         IN TXT "v=spf1 mx -all"
; public
@        IN A   198.51.100.11
www      IN A   198.51.100.11
shop     IN A   198.51.100.12
mail     IN A   198.51.100.13
ns1      IN A   198.51.100.14
vpn      IN A   198.51.100.15
; internal (should never be in the public zone)
fw       IN A   172.20.20.1
files    IN A   172.20.20.10
intranet IN A   172.20.20.11
nas      IN A   172.20.20.12
hr-pc    IN A   172.20.20.20
metasploitable2 IN A 172.20.20.30
cam01    IN A   172.20.30.10
printer  IN A   172.20.30.11
hvac     IN A   172.20.30.12
E
named-checkzone acme.lab /etc/bind/db.acme.lab >/dev/null
systemctl restart named
