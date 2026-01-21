#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e 

# Wait for the database to be ready before proceeding
python manage.py wait_for_db

# Collect static files into the STATIC_ROOT directory without user input
python manage.py collectstatic --noinput

# Apply database migrations to ensure the database schema is up to date
python manage.py migrate

# Start the uWSGI application server with specified configurations
# - Listen on socket :9000
# - Use 4 worker processes
# - Run in master mode
# - Enable threading
# - Load the WSGI application from the app.wsgi module
uwsgi --socket :8000 --workers 4 --master --enable-threads --module app.wsgi