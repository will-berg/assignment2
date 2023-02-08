#!/bin/bash
cd $(dirname $0)

./git_main.sh

../build.sh
. ../venv/bin/activate
../reload.sh
deactivate
