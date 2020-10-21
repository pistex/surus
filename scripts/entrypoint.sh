#!/bin/sh
python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
gunicorn --bind 0.0.0.0:$PORT --reload surus.wsgi:application
exec "$@"