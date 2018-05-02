import os
import sys
from cStringIO import StringIO


def save_stderr():
    # GTK likes to spam stderr, which inkscape will show in a dialog.
    null = open(os.devnull, 'w')
    sys.stderr_dup = os.dup(sys.stderr.fileno())
    os.dup2(null.fileno(), 2)
    sys.stderr_backup = sys.stderr
    sys.stderr = StringIO()


def restore_stderr():
    os.dup2(sys.stderr_dup, 2)
    sys.stderr_backup.write(sys.stderr.getvalue())
    sys.stderr = sys.stderr_backup
