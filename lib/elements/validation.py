from ..utils import Point


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
        self.position = Point(*position)

    def __eq__(self, other):
        return (self.name, self.description, self.position) == (other.name, other.description, other.position)

    def __hash__(self):
        return hash((self.name, self.description, self.position))