# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
from pathlib import Path  # to work with paths as objects
import configparser       # to read DEBUG.ini

# this file is without: import inkex
# - we need dump argv and sys.path as is on startup from inkscape
#   - later sys.path may be modified that influences importing inkex (see prefere_pip_inkex)


def write_offline_debug_script(debug_script_dir: Path, ini: configparser.ConfigParser):
    '''
    prepare Bash script for offline debugging from console
        arguments:
        - debug_script_dir - Path object, absolute path to directory of inkstitch.py
        - ini       - see DEBUG.ini
    '''

    # define names of files used by offline Bash script
    bash_file_base = ini.get("DEBUG", "bash_file_base", fallback="debug_inkstitch")
    bash_name = Path(bash_file_base).with_suffix(".sh")  # Path object
    bash_svg = Path(bash_file_base).with_suffix(".svg")  # Path object

    # check if input svg file exists in arguments, take argument that not start with '-' as file name
    svgs = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
    if len(svgs) != 1:
        print(f"WARN: {len(svgs)} svg files found, expected 1, [{svgs}]. No script created in write debug script.", file=sys.stderr)
        return

    svg_file = Path(svgs[0])
    if svg_file.exists() and bash_svg.exists() and bash_svg.samefile(svg_file):
        print("WARN: input svg file is same as output svg file. No script created in write debug script.", file=sys.stderr)
        return

    import shutil  # to copy svg file
    bash_file = debug_script_dir / bash_name

    with open(bash_file, 'w') as f:  # "w" text mode, automatic conversion of \n to os.linesep
        f.write('#!/usr/bin/env bash\n')

        # cmd line arguments for debugging and profiling
        f.write(bash_parser())  # parse cmd line arguments: -d -p

        f.write(f'# python version: {sys.version}\n')   # python version

        myargs = " ".join(sys.argv[1:])
        f.write(f'# script: {sys.argv[0]}  arguments: {myargs}\n')  # script name and arguments

        # environment PATH
        f.write('# PATH:\n')
        f.write(f'#   {os.environ.get("PATH","")}\n')
        # for p in os.environ.get("PATH", '').split(os.pathsep): # PATH to list
        #     f.write(f'#   {p}\n')

        # python module path
        f.write('# python sys.path:\n')
        for p in sys.path:
            f.write(f'#   {p}\n')

        # see static void set_extensions_env() in inkscape/src/inkscape-main.cpp
        f.write('# PYTHONPATH:\n')
        for p in os.environ.get('PYTHONPATH', '').split(os.pathsep):  # PYTHONPATH to list
            f.write(f'#   {p}\n')

        f.write(f'# copy {svg_file} to {bash_svg}\n#\n')
        shutil.copy(svg_file, debug_script_dir / bash_svg)  # copy file to bash_svg
        myargs = myargs.replace(str(svg_file), str(bash_svg))  # replace file name with bash_svg

        # see void Extension::set_environment() in inkscape/src/extension/extension.cpp
        f.write('# Export inkscape environment variables:\n')
        notexported = ['SELF_CALL']  # if an extension calls inkscape itself
        exported = ['INKEX_GETTEXT_DOMAIN', 'INKEX_GETTEXT_DIRECTORY',
                    'INKSCAPE_PROFILE_DIR', 'DOCUMENT_PATH', 'PYTHONPATH']
        for k in notexported:
            if k in os.environ:
                f.write(f'#   export {k}="{os.environ[k]}"\n')
        for k in exported:
            if k in os.environ:
                f.write(f'export {k}="{os.environ[k]}"\n')

        f.write('# signal inkstitch.py that we are running from offline script\n')
        f.write('export INKSTITCH_OFFLINE_SCRIPT="True"\n')

        f.write('# call inkstitch\n')
        f.write(f'python3 inkstitch.py {myargs}\n')
    bash_file.chmod(0o0755)  # make file executable, hopefully ignored on Windows


def bash_parser():
    return r'''
set -e   #  exit on error

# parse cmd line arguments:
#   -d enable debugging
#   -p enable profiling
#             ":..." - silent error reporting
while getopts ":dp" opt; do
  case $opt in
    d)
        export INKSTITCH_DEBUG_ENABLE="True"
        ;;
    p)
        export INKSTITCH_PROFILE_ENABLE="True"
        ;;
    \?)
        echo "Invalid option: -$OPTARG" >&2
        exit 1
        ;;
    :)
        echo "Option -$OPTARG requires an argument." >&2
        exit 1
        ;;
  esac
done

'''


def reorder_sys_path():
    '''
    change sys.path to prefer pip installed inkex over inkscape bundled inkex
    '''

    # see static void set_extensions_env() in inkscape/src/inkscape-main.cpp
    # what we do:
    # - move inkscape extensions path to the end of sys.path
    # - we compare PYTHONPATH with sys.path and move PYTHONPATH to the end of sys.path
    #   - also user inkscape extensions path is moved to the end of sys.path - may cause problems?
    #   - path for deprecated-simple are removed from sys.path, will be added later by importing inkex

    # PYTHONPATH to list
    pythonpath = os.environ.get('PYTHONPATH', '').split(os.pathsep)
    # remove pythonpath from sys.path
    sys.path = [p for p in sys.path if p not in pythonpath]
    # remove deprecated-simple, it will be added later by importing inkex
    pythonpath = [p for p in pythonpath if not p.endswith('deprecated-simple')]
    # remove nonexisting paths
    pythonpath = [p for p in pythonpath if os.path.exists(p)]
    # add pythonpath to the end of sys.path
    sys.path.extend(pythonpath)


# -----------------------------------------------------------------------------
# try to resolve debugger type from ini file or cmd line of bash
def resolve_debug_type(ini: configparser.ConfigParser):
    # enable/disable debugger from bash: -d
    if os.environ.get('INKSTITCH_DEBUG_ENABLE', '').lower() in ['true', '1', 'yes', 'y']:
        debug_enable = True
    else:
        debug_enable = ini.getboolean("DEBUG", "debug_enable", fallback=False)  # enable debugger on startup from ini

    debug_type = ini.get("DEBUG", "debug_type", fallback="none")  # debugger type vscode, pycharm, pydevd
    if not debug_enable:
        debug_type = 'none'

    debug_to_file = ini.getboolean("DEBUG", "debug_to_file", fallback=False)  # write debug output to file
    if debug_to_file and debug_type == 'none':
        debug_type = 'file'

    return debug_type


# try to resolve profiler type from ini file or cmd line of bash
def resolve_profile_type(ini: configparser.ConfigParser):
    # enable/disable profiling from bash: -p
    if os.environ.get('INKSTITCH_PROFILE_ENABLE', '').lower() in ['true', '1', 'yes', 'y']:
        profile_enable = True
    else:
        profile_enable = ini.getboolean("PROFILE", "profile_enable", fallback=False)  # read from ini

    # specify profiler type
    profiler_type = ini.get("PROFILE", "profiler_type", fallback="none")  # profiler type cprofile, profile, pyinstrument
    if not profile_enable:
        profiler_type = 'none'

    return profiler_type

# -----------------------------------------------------------------------------

# Profilers:
# currently supported profilers:
# - cProfile - standard python profiler
# - profile  - standard python profiler
# - pyinstrument - profiler with nice html output


def profile(profiler_type, profile_dir: Path, ini: configparser.ConfigParser, extension, remaining_args):
    '''
    profile with cProfile, profile or pyinstrument
    '''
    profile_file_base = ini.get("PROFILE", "profile_file_base", fallback="debug_profile")
    profile_file_path = profile_dir / profile_file_base  # Path object

    if profiler_type == 'cprofile':
        with_cprofile(extension, remaining_args, profile_file_path)
    elif profiler_type == 'profile':
        with_profile(extension, remaining_args, profile_file_path)
    elif profiler_type == 'pyinstrument':
        with_pyinstrument(extension, remaining_args, profile_file_path)
    else:
        raise ValueError(f"unknown profiler type: '{profiler_type}'")


def with_cprofile(extension, remaining_args, profile_file_path):
    '''
    profile with cProfile
    '''
    import cProfile
    import pstats
    profiler = cProfile.Profile()

    profiler.enable()
    extension.run(args=remaining_args)
    profiler.disable()

    profiler.dump_stats(profile_file_path.with_suffix(".prof"))  # can be read by 'snakeviz -s' or 'pyprof2calltree'
    with open(profile_file_path, 'w') as stats_file:
        stats = pstats.Stats(profiler, stream=stats_file)
        stats.sort_stats(pstats.SortKey.CUMULATIVE)
        stats.print_stats()
    print(f"Profiler: cprofile, stats written to '{profile_file_path.name}' and '{profile_file_path.name}.prof'. Use snakeviz to see it.",
          file=sys.stderr)


def with_profile(extension, remaining_args, profile_file_path):
    '''
    profile with profile
    '''
    import profile
    import pstats
    profiler = profile.Profile()

    profiler.run('extension.run(args=remaining_args)')

    profiler.dump_stats(profile_file_path.with_suffix(".prof"))  # can be read by 'snakeviz' or 'pyprof2calltree' - seems broken
    with open(profile_file_path, 'w') as stats_file:
        stats = pstats.Stats(profiler, stream=stats_file)
        stats.sort_stats(pstats.SortKey.CUMULATIVE)
        stats.print_stats()
    print(f"'Profiler: profile, stats written to '{profile_file_path.name}' and '{profile_file_path.name}.prof'. Use of snakeviz is broken.",
          file=sys.stderr)


def with_pyinstrument(extension, remaining_args, profile_file_path):
    '''
    profile with pyinstrument
    '''
    import pyinstrument
    profiler = pyinstrument.Profiler()

    profiler.start()
    extension.run(args=remaining_args)
    profiler.stop()

    profile_file_path = profile_file_path.with_suffix(".html")
    with open(profile_file_path, 'w') as stats_file:
        stats_file.write(profiler.output_html())
    print(f"Profiler: pyinstrument, stats written to '{profile_file_path.name}'. Use browser to see it.", file=sys.stderr)
