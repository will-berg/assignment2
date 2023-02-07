#!/bin/bash
cd $(dirname $0)

./kill.sh

./git_main.sh

cd ..
./build.sh
. venv/bin/activate
./run.sh
deactivate
