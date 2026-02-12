#!/bin/bash
# Azure App Service startup command
# This script is executed when the container starts

set -e

echo "Starting LinkedIn KPI Application on Azure App Service..."

# Navigate to the application directory
cd /home/site/wwwroot

# Set production environment variables
export ENVIRONMENT=production
export PORT=${PORT:-8000}

# Start Gunicorn with Uvicorn workers
echo "Starting Gunicorn server..."
exec gunicorn -c gunicorn.conf.py \
    --bind 0.0.0.0:${PORT} \
    --workers ${GUNICORN_WORKERS:-4} \
    --worker-class uvicorn.workers.UvicornWorker \
    --access-logfile - \
    --error-logfile - \
    asgi:application
