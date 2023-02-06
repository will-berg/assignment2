#!/bin/bash
python -m venv venv
. venv/bin/activate
pip install gunicorn
pip install -r requirements.txt
deactivate
