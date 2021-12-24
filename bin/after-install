#!/bin/sh

inkscape_dir="$(inkscape --system-data-directory)"

if [ "$?" != 0 ]; then
  echo "ERROR: Cannot find inkscape system data directory.  Is inkscape installed and in root's PATH?"
  exit 1
fi

rm -f "${inkscape_dir}/extensions/inkstitch"
ln -s /opt/inkstitch "${inkscape_dir}/extensions/inkstitch"
