#!/bin/bash
cd $(dirname $0)

./git_main.sh

cd ..
./build.sh
cd util
./reload.sh
