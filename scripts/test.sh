#!/bin/bash
cd $(dirname $0)
cd ..
[[ -z $VIRTUAL_ENV ]] && . venv/bin/activate
python3 -m unittest tests/ci_server.py
python3 -m unittest tests/updater.py
