# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
from pathlib import Path

# this file is without: import inkex
# - so we can modify sys.path before importing inkex

# DEBUG and PROFILE are in DEVEL.ini file

# DEBUG file format:
#  - first non-comment line is debugger type
#  - valid values are: 
#       "vscode" or "vscode-script"     - for debugging with vscode
#       "pycharm" or "pycharm-script"   - for debugging with pycharm
#       "pydev" or "pydev-script"       - for debugging with pydev
#       "none" or empty file            - for no debugging
#  - for offline debugging without inkscape, set debugger name to
#    as "vscode-script" or "pycharm-script" or "pydev-script"
#    - in that case running from inkscape will not start debugger
#      but prepare script for offline debugging from console
#    - valid for "none-script" too
#  - backward compatibilty is broken due to confusion
#      debug_type = 'pydev'                      # default debugger backwards compatibility
#      if 'PYCHARM_REMOTE_DEBUG' in os.environ:  # backwards compatibility
#         debug_type = 'pycharm'

# PROFILE file format:
#  - first non-comment line is profiler type
#  - valid values are:
#        "cprofile"                     - for cProfile
#        "pyinstrument"                 - for pyinstrument
#        "profile"                      - for profile
#        "none"                         - for no profiling


def parse_file(filename):
    # parse DEBUG or PROFILE file for type
    # - return first noncomment and nonempty line from file
    value_type = 'none'
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().lower()
            if line.startswith("#") or line == "": # skip comments and empty lines
                continue
            value_type = line    # first non-comment line is type
            break
    return value_type

def write_offline_debug_script(SCRIPTDIR : Path, bash_name : Path, bash_svg : Path):
    # prepare script for offline debugging from console

    # check if input svg file exists in arguments, take argument that not start with '-' as file name
    svgs = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
    if len(svgs) != 1:
        print(f"WARN: {len(svgs)} svg files found, expected 1, [{svgs}]. No script created in write debug script.", file=sys.stderr)
        return

    svg_file = Path(svgs[0])
    if svg_file.exists() and bash_svg.exists() and bash_svg.samefile(svg_file):
        print(f"WARN: input svg file is same as output svg file. No script created in write debug script.", file=sys.stderr)
        return
    
    import shutil
    bash_file = SCRIPTDIR / bash_name

    with open(bash_file, 'w') as f:  # "w" text mode, automatic conversion of \n to os.linesep
        f.write(f"#!/usr/bin/env bash\n\n")
        f.write(f"# python version: {sys.version}\n")   # python version
        
        myargs = " ".join(sys.argv[1:])
        f.write(f'# script: {sys.argv[0]}  arguments: {myargs}\n') # script name and arguments

        # python module path
        f.write(f"# python sys.path:\n")
        for p in sys.path:
            f.write(f"#   {p}\n")

        # see static void set_extensions_env() in inkscape/src/inkscape-main.cpp
        f.write(f"# PYTHONPATH:\n")
        for p in os.environ.get('PYTHONPATH', '').split(os.pathsep): # PYTHONPATH to list
            f.write(f"#   {p}\n")

        f.write(f"# copy {svg_file} to {bash_svg}\n")
        # check if files are not the same
        if svg_file != bash_svg:
            shutil.copy(svg_file, SCRIPTDIR / bash_svg)  # copy file to bash_svg
        myargs = myargs.replace(str(svg_file), str(bash_svg))   # replace file name with bash_svg

        # see void Extension::set_environment() in inkscape/src/extension/extension.cpp
        notexported = ["SELF_CALL"] # if an extension calls inkscape itself
        exported = ["INKEX_GETTEXT_DOMAIN", "INKEX_GETTEXT_DIRECTORY", 
                    "INKSCAPE_PROFILE_DIR", "DOCUMENT_PATH", "PYTHONPATH"]
        for k in notexported:
            if k in os.environ:
                f.write(f'# export {k}="{os.environ[k]}"\n')
        for k in exported:
            if k in os.environ:
                f.write(f'export {k}="{os.environ[k]}"\n')

        f.write('# signal inkstitch.py that we are running from offline script\n')
        f.write(f'export INKSTITCH_OFFLINE_SCRIPT="True"\n')

        f.write('# call inkstitch\n')
        f.write(f"python3 inkstitch.py {myargs}\n")
    bash_file.chmod(0o0755)  # make file executable
