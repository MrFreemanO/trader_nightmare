#!/bin/bash
cd /home/user/webapp/backend
source venv/bin/activate
export FLASK_APP=main.py
export FLASK_ENV=production
python main.py