import os
import sys
from io import StringIO


def save_stderr():
    # GTK likes to spam stderr, which inkscape will show in a dialog.
    with open(os.devnull, 'w') as null:
        sys.stderr_dup = os.dup(sys.stderr.fileno())
        sys.real_stderr = os.fdopen(sys.stderr_dup, 'w')
        os.dup2(null.fileno(), 2)
        sys.stderr = StringIO()


def restore_stderr():
    os.dup2(sys.stderr_dup, 2)
    sys.real_stderr.write(sys.stderr.getvalue())
    sys.stderr = sys.real_stderr

# It's probably possible to generalize this code, but when I tried,
# the result was incredibly unreadable.


def save_stdout():
    with open(os.devnull, 'w') as null:
        sys.stdout_dup = os.dup(sys.stdout.fileno())
        sys.real_stdout = os.fdopen(sys.stdout_dup, 'w')
        os.dup2(null.fileno(), 1)
        sys.stdout = StringIO()


def restore_stdout():
    os.dup2(sys.stdout_dup, 1)
    sys.real_stdout.write(sys.stdout.getvalue())
    sys.stdout = sys.real_stdout
