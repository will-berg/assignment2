#!/bin/bash
cd $(dirname $0)

./git_main.sh

cd ..
./build.sh
. venv/bin/activate
./reload.sh
deactivate
