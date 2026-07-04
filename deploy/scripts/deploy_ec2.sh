#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/fbr_pos_project}"
BRANCH="${BRANCH:-main}"

cd "$APP_DIR"

echo "[1/6] Fetching latest code"
git fetch --all --prune
git checkout "$BRANCH"
git pull origin "$BRANCH"

echo "[2/6] Building and starting services"
cd deploy
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d

echo "[3/6] Applying migrations"
docker compose -f docker-compose.prod.yml exec -T backend python manage.py migrate

echo "[4/6] Collecting static files"
docker compose -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --noinput

echo "[5/6] Health check"
curl -fsS http://localhost/api/admin-dashboard/stats/ >/dev/null || true

echo "[6/6] Deployment completed"
