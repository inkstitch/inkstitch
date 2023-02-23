# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from flask.json.provider import DefaultJSONProvider
from ..exceptions import InkstitchException


class InkstitchJSONException(InkstitchException):
    pass


class InkStitchJSONProvider(DefaultJSONProvider):
    """JSON encoder class that runs __json__ on an object if available.

    The __json__ method should return a JSON-compatible representation of the
    object.
    """

    def default(self, obj):
        try:
            return obj.__json__()
        except AttributeError:
            raise InkstitchJSONException(
                f"Object of type {obj.__class__.__name__} cannot be serialized to JSON because it does not implement __json__()")
