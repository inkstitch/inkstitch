#!/usr/bin/env bash

### Update uv to latest version with tools
### - Avoid frequent runs to prevent your IP address from being quickly banned.

### Update uv to latest version
uv self update

### Upgrade all tools
uv tool upgrade --all

