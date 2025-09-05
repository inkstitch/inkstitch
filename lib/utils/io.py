# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
from io import StringIO


def save_stderr():
    # GTK likes to spam stderr, which inkscape will show in a dialog.
    with open(os.devnull, 'w') as null:
        setattr(sys, 'stderr_dup', os.dup(sys.stderr.fileno()))
        setattr(sys, 'real_stderr', os.fdopen(getattr(sys, 'stderr_dup'), 'w', encoding='utf-8'))
        os.dup2(null.fileno(), 2)
        sys.stderr = StringIO()


def restore_stderr():
    stderr_dup = getattr(sys, 'stderr_dup', None)
    real_stderr = getattr(sys, 'real_stderr', None)
    if stderr_dup is not None and real_stderr is not None:
        os.dup2(stderr_dup, 2)
        if hasattr(sys.stderr, 'getvalue'):
            real_stderr.write(getattr(sys.stderr, 'getvalue')())
        sys.stderr = real_stderr

# It's probably possible to generalize this code, but when I tried,
# the result was incredibly unreadable.


def save_stdout():
    with open(os.devnull, 'w') as null:
        setattr(sys, 'stdout_dup', os.dup(sys.stdout.fileno()))
        setattr(sys, 'real_stdout', os.fdopen(getattr(sys, 'stdout_dup'), 'w'))
        os.dup2(null.fileno(), 1)
        sys.stdout = StringIO()


def restore_stdout():
    stdout_dup = getattr(sys, 'stdout_dup', None)
    real_stdout = getattr(sys, 'real_stdout', None)
    if stdout_dup is not None and real_stdout is not None:
        os.dup2(stdout_dup, 1)
        if hasattr(sys.stdout, 'getvalue'):
            real_stdout.write(getattr(sys.stdout, 'getvalue')())
        sys.stdout = real_stdout
