#!/bin/bash

# This is a self-extracting archive that installs Ink/Stitch on your Linux
# system.  This first part is an installer, and after that is a .tar.zx file
# containing Ink/Stitch itself.
#
# To install, simply run this script:
#
#   sh inkstitch-<version>.sh
#
#
# EXPERT STUFF BELOW:
#
# If you'd rather install it yourself, run this script with --extract to
# produce the original inkstitch-<version>.tar.xz file in the current
# directory.
#
# This script will attempt to determine where to install Inkscape user
# extensions automatically.  If it gets it wrong, you can set one of these
# environment variables:
#
#   INKSCAPE_PATH (ex: /usr/bin/inkscape)
#     The path to the inkscape executable program.  This script will ask that program 
#     where to install extensions by passing it the --user-data-directory argument.
#
#   INKSCAPE_EXTENSIONS_PATH (ex: $HOME/.config/inkscape/extensions)
#     The path to the inkscape extensions directory.  Use this to bypass the
#     --user-data-directory method and specify a directory yourself.

die() {
  echo "$*"
  exit 1
}

extract() {
  ( grep -m1 '^__ARCHIVE__$' > /dev/null; cat ) < "$0"
}

find_inkscape() {
  # allow expert user override
  if [ -n "$INKSCAPE_PATH" ]; then
    echo "$INKSCAPE_PATH"
    return
  fi

  inkscape="$(which inkscape)"

  if [ -z "$inkscape" ]; then
    read -p "Please enter the path to the inkscape program executable (example: /usr/bin/inkscape): " inkscape
  fi

  if [ ! -x "$inkscape" ]; then
    die "Inkscape not found or not executable ($inkscape)"
  fi

  echo "$inkscape"
}

find_extensions_dir() {
  # allow expert user override
  if [ -n "$INKSCAPE_EXTENSIONS_PATH" ]; then
    echo "$INKSCAPE_EXTENSIONS_PATH"
    return
  fi

  inkscape="$(find_inkscape)"

  if [ -x "$inkscape" ]; then
    extensions_dir="$(inkscape --user-data-directory)/extensions"
  fi

  if [ -z "$extensions_dir" ]; then
    read -p "Please enter the inkscape user extensions directory (example: $HOME/.config/inkscape/extensions): " extensions_dir
  fi

  if [ -z "$extensions_dir" ]; then
    die "Aborting."
  fi

  mkdir -p "$extensions_dir" || die "unable to create $extensions_dir"

  echo "$extensions_dir"
}

remove_existing() {
  if [ -e "${1}/inkstitch" ]; then
    read -p "${1}/inkstitch exists already.  It must be removed in order to install $(basename ${0%.sh}).  Delete? [y/N] " yesno
    if [ "$yesno" != "y" -a "$yesno" != "Y" -a "$yesno" != "yes" ]; then
      die "Aborting."
    fi

    rm -rf "${1}/inkstitch"
  fi
}

install_inkstitch() {
  extensions_dir="$(find_extensions_dir)"
  echo "Installing Ink/Stitch to ${extensions_dir}/inkstitch"

  remove_existing "$extensions_dir"

  extract | tar -C "$extensions_dir" -Jxf - || die "error while extracting Ink/Stitch"

  echo "Ink/Stitch has been successfully installed.  Please restart Inkscape if it is already running."
}

if [ "$1" = "--extract" ]; then
  dest="${0%.sh}.tar.xz"
  extract > "$dest"
  echo "Ink/Stitch extracted to $dest"
else
  install_inkstitch
fi

exit 0

__ARCHIVE__
