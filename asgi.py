"""
ASGI config for LinkedIn KPI FastHTML application.

This module exposes the ASGI callable as a module-level variable named ``application``.

Use this for production deployments with ASGI servers like Uvicorn, Gunicorn, or Hypercorn:
    - uvicorn asgi:application
    - gunicorn -k uvicorn.workers.UvicornWorker asgi:application
    - gunicorn -c gunicorn.conf.py asgi:application
"""

from main import app

# Create the application instance for ASGI servers
application = app

# Alias for different naming conventions
app = application
