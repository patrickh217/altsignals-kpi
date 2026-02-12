"""
Application entry point for Azure App Service
Serves FastHTML ASGI app via uvicorn worker class in startup.sh
"""
from main import app

__all__ = ['app']
