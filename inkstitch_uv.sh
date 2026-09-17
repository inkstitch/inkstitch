#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
uv --project "$SCRIPT_DIR" run python "$SCRIPT_DIR/inkstitch.py" $@
