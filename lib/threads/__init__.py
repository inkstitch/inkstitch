# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from importlib import import_module


_EXPORT_MODULES = {
    "ThreadCatalog": ".catalog",
    "ThreadColor": ".color",
    "ThreadPalette": ".palette",
}

__all__ = list(_EXPORT_MODULES)


def __getattr__(name):
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = import_module(module_name, __name__)
    exported_object = getattr(module, name)
    globals()[name] = exported_object
    return exported_object
