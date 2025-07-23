#!/usr/bin/env bash

# This script is used to run the Ink/Stitch extension for Inkscape.
# It sets up the virtual environment and calls the main Python script.
# Called directly from the Inkscape inx files in development mode.

# script position
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# uvr - activate the virtual environment relative to the script inkstitch.py directory
# - all args are passed to the script - $@,
# - working directory is relative to .svg file
uvr $SCRIPT_DIR/inkstitch.py "$@"


