#!/bin/bash

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuser --noinput \
  --username "$DJANGO_SUPERUSER_USERNAME" \
  --email "$DJANGO_SUPERUSER_EMAIL" \
  2>/dev/null || echo "Superuser already exists"

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application
