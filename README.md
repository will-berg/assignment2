# Assignment 2

## BUILD

To build the program, execute `./scripts/build.sh`
To lint, test and run, you have to activate the venv by running `. venv/bin/activate`. The venv can then be deactivated using `deactivate`.

## LINT
To lint the program, execute `./scripts/lint.sh`

## TEST
To test the program, execute `./scripts/test.sh`

## RUN
To run the program, execute `./scripts/run.sh <output dir>`, where `<output dir>` is the directory where you want to store and serve the build output. `./scripts/run.sh` will start the CI server, the auto updater and the web server.

## BUILD LIST
A list of all builds can be found at `http://molly.aronbergman.se`

## WAY OF WORKING/ESSENCE
The reflection of our way of working according to Essence is available in the `docs` folder.

## STATEMENT OF CONTRIBUTIONS
Filippa: Worked on the GitHub status API. Also worked on writing all outputs to file.

Aron: Mainly worked on the auto updater and shell scripts and operated the server running the software.

Peter: Worked on the web service, some documentation and helped with process spawning and killing.

Salome: Worked on ci_server control flow, set up the tests, listing of the builds and Essence report. 

William: Worked on ci_server control flow, file operations, and pipeline functions. Also worked on documentation with Pydoc.
