# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
from typing import List, Any

from shapely.geometry import Point as ShapelyPoint

from ..utils import Point as InkstitchPoint


class ValidationMessage(object):
    '''Holds information about a problem with an element.

    Attributes:
      name - A short descriptor for the problem, such as "dangling rung"
      description - A detailed description of the problem, such as
        "One or more rungs does not intersect both rails."
      position - An optional position where the problem occurs,
        to aid the user in correcting it.  type: Point or tuple of (x, y)
      steps_to_solve - A list of operations necessary to solve the problem
    '''

    # Subclasses will fill these in.
    name = None
    description = None
    steps_to_solve: List[Any] = []

    def __init__(self, position=None, label=""):
        if isinstance(position, ShapelyPoint):
            position = (position.x, position.y)

        self.position = InkstitchPoint(*position)
        self.label = label


class ValidationError(ValidationMessage):
    """A problem that will prevent the shape from being embroidered."""
    pass


class ValidationWarning(ValidationMessage):
    """A problem that won't prevent a shape from being embroidered.

    The user will almost certainly want to fix the warning, but if they
    don't, Ink/Stitch will do its best to process the object.
    """
    pass


class ObjectTypeWarning(ValidationMessage):
    """A shape is not a path and will not be embroidered.

    Ink/Stitch only works with paths and ignores everything else.
    The user might want the shape to be ignored, but if they
    don't, they receive information how to change this behaviour.
    """
    pass
