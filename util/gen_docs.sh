#!/bin/bash
cd $(dirname $0)

cd ..
python -m pydoc -w ci_server
python -m pydoc -w updater
python -m pydoc -w web
mv *.html docs/
