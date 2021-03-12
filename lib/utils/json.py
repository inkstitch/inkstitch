# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from flask.json import JSONEncoder


class InkStitchJSONEncoder(JSONEncoder):
    """JSON encoder class that runs __json__ on an object if available.

    The __json__ method should return a JSON-compatible representation of the
    object.
    """

    def default(self, obj):
        try:
            return obj.__json__()
        except AttributeError:
            return JSONEncoder.default(self, obj)
