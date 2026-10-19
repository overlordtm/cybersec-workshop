# shop.acme.lab - OWASP Juice Shop (exercise 3.3: requests, forms, cookies)
docker rm -f shop 2>/dev/null || true
docker run -d --name shop --restart unless-stopped -p 80:3000 bkimminich/juice-shop:v20.3.0
