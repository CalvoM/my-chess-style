#!/bin/sh
set -e

. /app/.venv/bin/activate
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py import_chess_openings

exec python manage.py runserver 0.0.0.0:8000
