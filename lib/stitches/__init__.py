# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import importlib as _importlib

_STITCH_MAP = {
    'auto_fill': '.auto_fill',
    'circular_fill': '.circular_fill',
    'cross_stitch': '.cross_stitch',
    'legacy_fill': '.fill',
    'guided_fill': '.guided_fill',
    'linear_gradient_fill': '.linear_gradient_fill',
    'meander_fill': '.meander_fill',
    'tartan_fill': '.tartan_fill',
    'contour_fill': '.contour_fill',
    'running_stitch': '.running_stitch',
}


def __getattr__(name):
    if name in _STITCH_MAP:
        mod = _importlib.import_module(_STITCH_MAP[name], __name__)
        val = getattr(mod, name)
        globals()[name] = val
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Can't put this here because we get a circular import :(
# from .auto_satin import auto_satin
# from .ripple_stitch import ripple_stitch
