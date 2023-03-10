#!/bin/bash
cd $(dirname $0)
cd ..
[[ -z $VIRTUAL_ENV ]] && . venv/bin/activate
pip install pylint
pylint --errors-only ci_server.py
pylint --errors-only web.py
pylint --errors-only updater.py
