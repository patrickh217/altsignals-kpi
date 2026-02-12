"""
Application entry point for Azure App Service
Wraps the FastHTML ASGI app for WSGI using asgiref
"""
try:
    from asgiref.wsgi import ASGItoWSGI
    from main import app as asgi_app

    # Wrap ASGI app for WSGI compatibility with gunicorn
    app = ASGItoWSGI(asgi_app)
except ImportError:
    # Fallback if asgiref not available
    from main import app

__all__ = ['app']
