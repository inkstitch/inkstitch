#!/usr/bin/env bash

# Example of running a GitHub Action workflow from the command line.
# Install gh CLI: https://cli.github.com/
# Make sure you have the necessary permissions to trigger workflows.

set -e
set -x

# options:
#   build_type  - OS architecture
#   input_tag   - v* version tag
#   verbosity   - log level 0 - error, 1 - info, 2 - debug  3 - trace
#   sign        - authorized sign fow windows and notarize for mac
#   break_on    - break on uv, sync or no

WF=uv_build.yml

BR=`git rev-parse --abbrev-ref HEAD`


build_type='dummy'
# build_type='all'

# build_type='linux32'
# build_type='linux64'
# build_type='linuxarm64'
# build_type='macx86'
# build_type='macarm64'
# build_type='windows64'


# sign: true - authorized sign for windows and notarize for mac, false (default) - no windows sign and no mac notarize
# sign='true'

# input_tag
tag='v0.0.0-alpha'

break_on="no"
#break_on="uv"
#break_on="sync" # on exit cache is not updated !!!

# verbosity: 0 - error, 1 - info (default), 2 - debug, 3 - trace
log_level=1


#git commit -a -m "Automated Commit & Build"
#git push

### --------------------------------------------------------- run workflow

### common options
gh workflow run $WF -r $BR -f build_type=$build_type

### for v* rebuilds
# gh workflow run $WF -r $BR -f build_type=$build_type -f input_tag=$tag

### for v* rebuilds with authorized sign
# gh workflow run $WF -r $BR -f build_type='all' -f input_tag=$tag -f sign='true'

### developer options
# gh workflow run $WF -r $BR -f build_type=$build_type -f break_on=$break_on
# gh workflow run $WF -r $BR -f build_type=$build_type -f break_on=$break_on -f verbosity=$log_level

