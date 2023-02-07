#!/bin/bash
cd $(dirname $0)

./kill.sh

./git_main.sh

../build.sh
. ../venv/bin/activate
../run.sh
deactivate