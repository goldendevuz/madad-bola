#!/bin/bash

set -e  # Exit on any error

# Apply database migrations
make mig

# Collect static files
make collect

# Start the Gunicorn WSGI server with full logging
echo "Starting Gunicorn WSGI server..."
exec gunicorn core.wsgi:application \
  --bind 0.0.0.0:1025 \
  --workers 3 \
  --timeout 120 \
  --log-level info \
  --access-logfile - \
  --error-logfile -
