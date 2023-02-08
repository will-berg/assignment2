#!/bin/bash
git checkout main
git fetch
git reset --hard origin/main
git clean -fdx -e github_token.py
