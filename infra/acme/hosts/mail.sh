# mail.acme.lab - Postfix (SMTP, submission) and Dovecot (POP3, IMAP, IMAPS) with version banners
echo "postfix postfix/main_mailer_type select Internet Site" | debconf-set-selections
echo "postfix postfix/mailname string acme.lab" | debconf-set-selections
DEBIAN_FRONTEND=noninteractive apt-get -y -qq install postfix dovecot-imapd dovecot-pop3d >/dev/null
postconf -e 'myhostname = mail.acme.lab' 'mydomain = acme.lab' 'smtpd_banner = $myhostname ESMTP Postfix (Debian/GNU)' \
    'inet_interfaces = all' 'mydestination = acme.lab, mail.acme.lab, localhost'
sed -i 's/^#submission inet/submission inet/' /etc/postfix/master.cf
cat > /etc/dovecot/conf.d/99-acme.conf <<'E'
login_greeting = ACME mail (Dovecot) ready.
protocols = imap pop3
E
for u in janez.novak maja.kovac peter.horvat ana.krajnc podpora info; do id "$u" >/dev/null 2>&1 || useradd -m -s /usr/sbin/nologin "$u"; done
systemctl restart postfix dovecot
