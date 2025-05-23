#!/usr/bin/env bash

### !!! before running this script, install uv and the tools: see bin/uv/tools_install.sh
### !!! run this script in the root of your project
### !!! - copy this to your local copy

### set python version, create .python-version file
uv python pin 311

### create virtual environment
uv venv

### create pyproject.toml file
bin/uv/generate_pyproject.sh
# bin/uv/generate_pyproject.sh -n   # dont detect packages, will set manually later

### Manually add packages to pyproject.toml

### wxPython for Linux - requires to check python version and OS
# uv add "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/wxpython-4.2.3-cp39-cp39-linux_x86_64.whl"
# uv add "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/wxpython-4.2.3-cp311-cp311-linux_x86_64.whl"

###
# uv add "pygobject<=3.50"

### Here put your packages
# uv add mypkg

### install packages from pyproject.toml
# uv sync
