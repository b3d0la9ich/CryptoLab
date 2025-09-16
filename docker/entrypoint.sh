#!/bin/sh
set -e
flask db upgrade
python manage.py create_admin_if_needed
exec flask run --host=0.0.0.0 --port=8000
