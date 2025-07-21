#!/usr/bin/env bash

# script position
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

### DEBUG: all args to file are passed to the script,
###        working directory is relative to .svg file

uvr $SCRIPT_DIR/inkstitch.py "$@"


