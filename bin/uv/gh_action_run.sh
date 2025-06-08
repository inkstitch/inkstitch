#!/usr/bin/env bash

# Example of running a GitHub Action workflow from the command line.
# Install gh CLI: https://cli.github.com/
# Make sure you have the necessary permissions to trigger workflows.

### - Avoid frequent runs to prevent your IP address from being quickly banned.


set -x

WF=uv_build.yml
BR=`git rev-parse --abbrev-ref HEAD`

build_type='dummy'
# build_type='linux32'
# build_type='linux64'
# build_type='linuxarm64'
# build_type='macarm64'
# build_type='macx86'
# build_type='windows64'
# build_type='all'

# break_on="no"
# break_on="uv"
# break_on="sync" # on exit cache is not updated !!!

# tag='dev-build-$BR'

# git commit -a -m "Automated Commit & Build"
# git push

### gh workflow run $WF -r $BR -f build_type=$build_type
### gh workflow run $WF -r $BR -f build_type=$build_type -f break_on=$break_on -f input_tag=$tag
# gh workflow run $WF -r $BR -f build_type=$build_type -f break_on=$break_on




