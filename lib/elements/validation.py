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
      steps to solve - A list of operations necessary to solve the problem
    '''

    def __init__(self, name, description, position=None, steps_to_solve=None):
        self.name = name
        self.description = description
        self.steps_to_solve = []

        if steps_to_solve:
            self.steps_to_solve = steps_to_solve

        if isinstance(position, ShapelyPoint):
            position = (position.x, position.y)

        self.position = InkstitchPoint(*position)

    # These two methods allow us to gather up errors by type in a dict or set
    def __eq__(self, other):
        return (self.name, self.description) == (other.name, other.description)

    def __hash__(self):
        return hash((self.name, self.description))
