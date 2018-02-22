#!/usr/bin/env python

import sys
import os
import subprocess

# ink/stitch
#
# stub.py: pyinstaller execution stub
#
# pyinstaller packages the inkstitch extensions into nice tidy executables.
# That's great, but Inkscape can't execute a plain binary as an extension(!).
#
# This Python script exists only to execute the actual extension binary.  It
# can be copied to, e.g., "embroider_params.py", in which case it will look
# for a binary at inkstitch/bin/embroider_params.

script_name = os.path.basename(__file__)

if script_name.endswith('.py'):
    binary_name = script_name[:-3]
else:
    # Probably not right, but we can at least try.
    binary_name = script_name

binary_path = os.path.join("inkstitch", "bin", binary_name)

args = sys.argv[:]
args[0] = binary_path

# os.execve works here for Linux, but only this seems to get the
# extension output to Inkscape on Windows
extension = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = extension.communicate()
print stdout
print >> sys.stderr, stderr
sys.exit(extension.returncode)
