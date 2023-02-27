# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

def string_to_floats(string, delimiter=","):
    """Convert a string of delimiter-separated floats into a list of floats."""

    floats = string.split(delimiter)
    return [float(num) for num in floats if _is_float(num)]


def _is_float(float_string):
    try:
        float(float_string)
        return True
    except ValueError:
        return False


def remove_suffix(string, suffix):
    if string.endswith(suffix):
        return string[:-len(suffix)]
    else:
        return string
