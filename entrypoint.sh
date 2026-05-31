#!/bin/sh
set -e

if [ "$RUN_MIGRATIONS" = "1" ]; then
  echo "Running database migrations..."
  python manage.py migrate --noinput
fi

if [ "$COLLECT_STATIC" = "1" ]; then
  echo "Copying static files..."
  python manage.py collectstatic --noinput
fi

exec "$@"