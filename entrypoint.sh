#!/bin/bash
set -e

echo "running local server django gunicorn server.."
# gunicorn --bind 0.0.0.0:8080 --timeout 3600000 --workers=4 backend.wsgi:application 
python manage.py runserver 0:8080