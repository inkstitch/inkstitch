#!/usr/bin/env bash

### install uv:
###   see https://github.com/astral-sh/uv

### On macOS and Linux.
# curl -LsSf https://astral.sh/uv/install.sh | sh

### On Windows.
# powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

### update uv to latest version
uv self update


### install uvr
# uv tool install --from git+https://github.com/karnigen/uvr uvr

### tools required
### flake8 for style checking - see make style
# uv tool install flake8


### upgrade all tools
uv tool upgrade --all


### set python version, create .python-version file
uv python pin 39

### create virtual environment
uv venv

### preinstall packages that cannot be managed by pyproject.toml
### wxPython for Linux - check python version and OS
uv pip install https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/wxpython-4.2.3-cp39-cp39-linux_x86_64.whl

###
uv pip install "pygobject<=3.50"

### install packages from pyproject.toml
#uv sync --inexact
