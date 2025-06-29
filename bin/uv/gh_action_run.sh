#!/usr/bin/env bash

# Example of running a GitHub Action workflow from the command line.
# Install gh CLI: https://cli.github.com/
# Make sure you have the necessary permissions to trigger workflows.

set -e
set -x

# options:
#   build_type  - OS architecture
#   verbosity   - log level 0 - error, 1 - info, 2 - debug  3 - trace
#   sign        - authorized sign fow windows and notarize for mac
#   break_on    - break on uv, sync or no

WF=uv_build.yml

build_type='dummy'
# build_type='all'

# build_type='linux32'
# build_type='linux64'
# build_type='linuxarm64'
# build_type='macx86'
# build_type='macarm64'
# build_type='windows64'

### --------------------------------------------------------- select branch or tag
### You can select branch or tag to run the workflow on.
###   If you run the script on a branch, it will use the current branch.
###   If you run the script on a tag, it will use the tag name.

### build type: branch
REF=`git rev-parse --abbrev-ref HEAD`

### build type: tag
# REF='v0.0.0test'
# REF='v0.0.0test2'

### sign: true - authorized sign for windows and notarize for mac, false (default) - no windows sign and no mac notarize
# sign='true'

### --------------------------------------------------------- debug options

break_on="no"
# break_on="uv"
# break_on="sync" # on exit cache is not updated !!!

# verbosity: 0 - error, 1 - info (default), 2 - debug, 3 - trace
log_level=1

### Automatically commit and push changes to the repository.
# git commit -a -m "Automated Commit & Build"
# git push

### --------------------------------------------------------- run workflow

### for branch rebuilds
gh workflow run $WF -r $REF -f build_type=$build_type

### for v* rebuilds with authorized sign, set correct tag name
# gh workflow run $WF -r $REF -f build_type='all' -f sign='true'

### developer options
# gh workflow run $WF -r $REF -f build_type=$build_type -f break_on=$break_on
# gh workflow run $WF -r $REF -f build_type=$build_type -f break_on=$break_on -f verbosity=$log_level

