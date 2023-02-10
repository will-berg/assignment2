#!/bin/bash
cd $(dirname $0)
cd ..
python3 -m venv venv
. venv/bin/activate
pip install gunicorn
pip install -r requirements.txt
[ ! -f github_token.py ] && cat <<EOF > github_token.py
github_token = "your_token_here"
EOF
deactivate
