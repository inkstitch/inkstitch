#!/usr/bin/env bash

### Install common tools  for all platforms

### - install `uv`:  see https://github.com/astral-sh/uv
### - put `uv` on PATH

### On macOS and Linux.
# curl -LsSf https://astral.sh/uv/install.sh | sh

### On Windows.
# powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"


### Install uvr
uv tool install --from git+https://github.com/karnigen/uvr uvr

### Tools required
### flake8 for style checking - see make style
uv tool install flake8
### cmake for building C extensions
uv tool install cmake
