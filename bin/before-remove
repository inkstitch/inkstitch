#!/bin/sh

inkscape_dir="$(inkscape --system-data-directory)"

if [ -n "$inkscape_dir" ]; then
  if [ -L "${inkscape_dir}/extensions/inkstitch" ]; then
    rm -f "${inkscape_dir}/extensions/inkstitch"
  fi
fi
