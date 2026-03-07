#!/usr/bin/env bash
# Render build script — runs on every deploy

set -o errexit  # exit on error

pip install -r requirements.txt

python manage.py migrate --no-input

python manage.py collectstatic --no-input

# Re-enable / create the admin superuser using env variables
python manage.py ensure_admin

# Seed initial resource categories (safe to re-run)
python manage.py create_categories
