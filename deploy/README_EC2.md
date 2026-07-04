# EC2 Deployment Guide (No Load Balancer)

This setup runs each component separately:
- Postgres container
- Redis container
- Django backend container
- Celery worker container
- Celery beat container
- Vue frontend container
- Nginx reverse proxy container
- Certbot for SSL renewal

Production recommendation:
- Use AWS RDS for PostgreSQL (managed database).
- Keep the Postgres container only for local/testing fallback.

## 1. One-time server setup

1. Launch Ubuntu EC2 instance.
2. Open security group ports:
   - 22 (SSH)
   - 80 (HTTP)
   - 443 (HTTPS)
3. Install Docker and Docker Compose plugin.
4. Clone this repo to `/opt/fbr_pos_project`.

## 2. Prepare environment

1. Copy files:
   - `deploy/env/backend.env.example` -> `deploy/env/backend.env`
   - `deploy/env/postgres.env.example` -> `deploy/env/postgres.env`
2. Fill all secrets.
3. For RDS, set these in `deploy/env/backend.env`:
   - `DB_HOST=<your-rds-endpoint>`
   - `DB_PORT=5432`
   - `DB_NAME=<rds_db_name>`
   - `DB_USER=<rds_user>`
   - `DB_PASSWORD=<rds_password>`

## 3. Start stack

Run:

```
cd /opt/fbr_pos_project/deploy
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec -T backend python manage.py migrate
```

If you want to use local Postgres container instead of RDS:

```
cd /opt/fbr_pos_project/deploy
docker compose -f docker-compose.prod.yml --profile local-db up -d --build
docker compose -f docker-compose.prod.yml exec -T backend python manage.py migrate
```

## 4. SSL with Let's Encrypt

Important: Let's Encrypt requires a real domain name pointing to your EC2 public IP.
It cannot issue valid certs for raw IP addresses.

If you do not own a paid domain, use a free dynamic DNS provider (for example DuckDNS), then point that hostname to your EC2 IP.

After DNS points correctly, edit `deploy/nginx/app.conf` and replace `YOUR_DOMAIN`.

Issue certificate:

```
cd /opt/fbr_pos_project/deploy
docker compose -f docker-compose.prod.yml run --rm certbot certonly \
  --webroot -w /var/www/certbot \
  -d YOUR_DOMAIN \
  --email YOUR_EMAIL \
  --agree-tos --no-eff-email

docker compose -f docker-compose.prod.yml restart nginx
```

Renewal cron on EC2:

```
0 3 * * * cd /opt/fbr_pos_project/deploy && docker compose -f docker-compose.prod.yml run --rm certbot renew && docker compose -f docker-compose.prod.yml restart nginx
```

## 5. GitHub auto-deploy pipeline

Workflow file:
- `.github/workflows/ci-cd-ec2.yml`

Add repository secrets:
- `EC2_HOST`
- `EC2_USER`
- `EC2_SSH_KEY`
- `EC2_APP_DIR` (example: `/opt/fbr_pos_project`)

Pipeline flow:
1. Run backend checks.
2. Build frontend.
3. SSH into EC2.
4. Pull latest code.
5. Build and restart containers.
6. Run migrations and collectstatic.

## 6. Recommended production hardening

- Set `DEBUG=False`.
- Restrict `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
- Put DB and Redis in private subnets/VPC-only access if possible.
- Enable instance backups and S3 lifecycle rules.
- Store secrets in AWS SSM or GitHub encrypted secrets, never in git.
