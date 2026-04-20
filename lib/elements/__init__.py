# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import importlib as _importlib

_ELEMENT_MAP = {
    'Clone': ('.clone', 'Clone'),
    'EmbroideryElement': ('.element', 'EmbroideryElement'),
    'EmptyDObject': ('.empty_d_object', 'EmptyDObject'),
    'FillStitch': ('.fill_stitch', 'FillStitch'),
    'ImageObject': ('.image', 'ImageObject'),
    'SatinColumn': ('.satin_column', 'SatinColumn'),
    'Stroke': ('.stroke', 'Stroke'),
    'TextObject': ('.text', 'TextObject'),
    'iterate_nodes': ('.utils.nodes', 'iterate_nodes'),
    'node_to_elements': ('.utils.nodes', 'node_to_elements'),
    'nodes_to_elements': ('.utils.nodes', 'nodes_to_elements'),
}


def __getattr__(name):
    if name in _ELEMENT_MAP:
        module_path, attr_name = _ELEMENT_MAP[name]
        mod = _importlib.import_module(module_path, __name__)
        val = getattr(mod, attr_name)
        globals()[name] = val
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
