@echo off
REM This script runs the Ink/Stitch extension for Inkscape in development mode.
REM It sets up the virtual environment and calls the main Python script.
REM Called directly from the Inkscape INX files in development mode.

REM Get the directory of this script
set SCRIPT_DIR=%~dp0

REM uvr - activate the virtual environment relative to the inkstitch.py directory
REM All arguments are passed to the script: %*
REM Working directory is relative to the .svg file
uvr "%SCRIPT_DIR%inkstitch.py" %*
