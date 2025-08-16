#!/bin/bash
set -e

cd /home/user/webapp/backend
source venv/bin/activate

export FLASK_APP=main.py
export FLASK_ENV=production

# Use Gunicorn for production
gunicorn --workers 4 --bind 0.0.0.0:5000 main:app
