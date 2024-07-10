#!/bin/bash

VERSION="${GITHUB_REF##*/}"
OS="${BUILD:-$(uname)}"
DATE=$(date +"%Y-%m-%d %H:%M")
if [[ "$VERSION" == "" ]]; then
  VERSION="Manual Install"
fi

echo "${VERSION} (${OS}) ${DATE}" > VERSION
