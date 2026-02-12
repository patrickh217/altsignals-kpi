"""
Gunicorn configuration file for Azure App Service deployment.

This configuration optimizes the FastHTML application for production use with proper
worker management, logging, and performance settings.

Usage:
    gunicorn -c gunicorn.conf.py asgi:application
"""

import multiprocessing
import os

# =============================================================================
# Server Socket
# =============================================================================

bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}"
backlog = 2048

# Trust Azure App Service reverse proxy headers
forwarded_allow_ips = "*"

# =============================================================================
# Worker Processes
# =============================================================================

# Worker class - use uvicorn worker for ASGI applications
worker_class = "uvicorn.workers.UvicornWorker"

# Number of worker processes
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))

# Worker threads (for sync workers only, not used with uvicorn worker)
threads = 1

# Maximum number of requests a worker will process before restarting
max_requests = int(os.getenv("MAX_REQUESTS", 1000))
max_requests_jitter = 50

# Worker timeout in seconds
timeout = 120
keepalive = 5

# =============================================================================
# Logging
# =============================================================================

# Access log
accesslog = "-"  # Log to stdout
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Error log
errorlog = "-"  # Log to stderr
loglevel = os.getenv("LOG_LEVEL", "info").lower()

# Capture stdout/stderr in error log
capture_output = True

# =============================================================================
# Process Naming
# =============================================================================

proc_name = "linkedin-kpi"

# =============================================================================
# Server Mechanics
# =============================================================================

# Restart workers when code changes (only for development)
reload = os.getenv("DEBUG", "false").lower() == "true"

# Daemonize the Gunicorn process
daemon = False

# Directory to store temporary files
tmp_upload_dir = None

# =============================================================================
# Security
# =============================================================================

# Limit request line size
limit_request_line = 4096

# Limit request header field size
limit_request_field_size = 8190

# Limit number of request header fields
limit_request_fields = 100

# =============================================================================
# Server Hooks
# =============================================================================


def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting Gunicorn server")


def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Gunicorn server is ready. Spawning workers")


def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)
