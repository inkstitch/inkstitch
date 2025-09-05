# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from flask.json.provider import DefaultJSONProvider
from ..exceptions import InkstitchException
from typing import Any
import json


class InkstitchJSONException(InkstitchException):
    pass


class InkStitchJSONProvider(DefaultJSONProvider):
    """JSON encoder class that runs __json__ on an object if available.

    The __json__ method should return a JSON-compatible representation of the
    object.
    """

    def dumps(self, obj: Any, **kwargs: Any) -> str:
        """Override dumps to handle __json__ method."""
        try:
            # Try to use the object's __json__ method if available
            if hasattr(obj, '__json__'):
                obj = obj.__json__()
            return super().dumps(obj, **kwargs)
        except Exception:
            raise InkstitchJSONException(
                f"Object of type {type(obj).__name__} cannot be serialized to JSON")
