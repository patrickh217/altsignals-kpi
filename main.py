"""
Company Scraper Dashboard - Main Application Entry Point
A multi-platform analytics dashboard for web scraping operations
"""
from fasthtml.common import *
from components.styles import APP_STYLES
from routes.auth_routes import setup_auth_routes
from routes.platform_routes import setup_platform_routes
from routes.linkedin_routes import setup_linkedin_routes
from routes.system_routes import setup_system_routes


# Initialize FastHTML app with session support
app, rt = fast_app(
    hdrs=(
        Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js"),
        Style(APP_STYLES)
    )
)

# Setup all routes
setup_auth_routes(rt)
setup_platform_routes(rt)
setup_linkedin_routes(rt)
setup_system_routes(rt)

# Start the server
if __name__ == "__main__":
    serve()
