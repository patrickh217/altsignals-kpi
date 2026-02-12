#!/bin/bash
gunicorn --workers 1 --worker-class uvicorn.workers.UvicornWorker --timeout 600 --access-logfile \- --error-logfile \- --bind=0.0.0.0:8000 "main:app"
