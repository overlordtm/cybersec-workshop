# www.acme.lab - company website on an old Apache (2.4.49, CVE-2021-41773 in the banner;
# the default config denies access outside DocumentRoot, so the path traversal is not exploitable).
docker rm -f www 2>/dev/null || true
docker run -d --name www --restart unless-stopped --network host \
    -v /opt/acme/htdocs:/usr/local/apache2/htdocs:ro httpd:2.4.49
