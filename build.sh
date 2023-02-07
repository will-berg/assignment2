#!/bin/bash
python3 -m venv venv
. venv/bin/activate
pip install gunicorn
pip install -r requirements.txt
deactivate
