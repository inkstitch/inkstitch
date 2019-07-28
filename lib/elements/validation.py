from shapely.geometry import Point as ShapelyPoint

from ..utils import Point as InkstitchPoint


class ValidationError(object):
    '''Holds information about a problem with an element.

    Attributes:
      name - A short descriptor for the problem, such as "dangling rung"
      description - A detailed description of the problem, such as
        "One or more rungs does not intersect both rails."
      position - An optional position where the problem occurs,
        to aid the user in correcting it.  type: Point or tuple of (x, y)
    '''

    def __init__(self, name, description, position=None):
        self.name = name
        self.description = description

        if isinstance(position, ShapelyPoint):
            position = (position.x, position.y)

        self.position = InkstitchPoint(*position)

    # These two methods allow us to gather up errors by type in a dict or set
    def __eq__(self, other):
        return (self.name, self.description) == (other.name, other.description)

    def __hash__(self):
        return hash((self.name, self.description))
