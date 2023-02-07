#!/bin/bash
pip install pylint
pylint --errors-only ci_server.py
pylint --errors-only updater.py
