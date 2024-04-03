# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from shapely import geometry as shgeo

from ..utils.geometry import Point


class Stitch(Point):
    """A stitch is a Point with extra information telling how to sew it."""

    def __init__(
        self,
        x, y=None,
        color=None,
        jump=False,
        stop=False,
        trim=False,
        color_change=False,
        min_stitch_length=None,
        tags=None
    ):
        # DANGER: if you add new attributes, you MUST also set their default
        # values in __new__() below.  Otherwise, cached stitch plans can be
        # loaded and create objects without those properties defined, because
        # unpickling does not call __init__()!

        base_stitch = None
        if isinstance(x, Stitch):
            # Allow creating a Stitch from another Stitch.  Attributes passed as
            # arguments will override any existing attributes.
            base_stitch = x
            self.x: float = base_stitch.x
            self.y: float = base_stitch.y
        elif isinstance(x, (Point, shgeo.Point)):
            # Allow creating a Stitch from a Point
            point = x
            self.x: float = point.x
            self.y: float = point.y
        else:
            Point.__init__(self, x, y)

        self._set('color', color, base_stitch)
        self._set('jump', jump, base_stitch)
        self._set('trim', trim, base_stitch)
        self._set('stop', stop, base_stitch)
        self._set('color_change', color_change, base_stitch)
        self._set('min_stitch_length', min_stitch_length, base_stitch)

        self.tags = set()
        self.add_tags(tags or [])
        if base_stitch is not None:
            self.add_tags(base_stitch.tags)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        # Set default values for any new attributes here (see note in __init__() above)
        # instance.foo = None

        return instance

    def __repr__(self):
        return "Stitch(%s, %s, %s, %s, %s, %s, %s, %s)" % (
            self.x,
            self.y,
            self.color,
            self.min_stitch_length,
            "JUMP" if self.jump else " ",
            "TRIM" if self.trim else " ",
            "STOP" if self.stop else " ",
            "COLOR CHANGE" if self.color_change else " "
        )

    def _set(self, attribute, value, base_stitch):
        # Set an attribute.  If the caller passed a Stitch object, use its value, unless
        # they overrode it with arguments.
        if base_stitch is not None:
            setattr(self, attribute, getattr(base_stitch, attribute))
        if value or base_stitch is None:
            setattr(self, attribute, value)

    @property
    def is_terminator(self) -> bool:
        return self.trim or self.stop or self.color_change

    def add_tags(self, tags):
        for tag in tags:
            self.add_tag(tag)

    def add_tag(self, tag):
        """Store arbitrary information about a stitch.

        Tags can be used to store any information about a stitch.  This can be
        used by other parts of the code to keep track of where a Stitch came
        from.  The Stitch treats tags as opaque.

        Use strings as tags.  Python automatically optimizes this kind of
        usage of strings, and it doesn't have to constantly do string
        comparisons.  More details here:

          https://stackabuse.com/guide-to-string-interning-in-python
        """
        self.tags.add(tag)

    def has_tag(self, tag):
        return tag in self.tags

    def copy(self):
        return Stitch(
            self.x,
            self.y,
            self.color,
            self.jump,
            self.stop,
            self.trim,
            self.color_change,
            self.min_stitch_length,
            self.tags
        )

    def offset(self, offset: Point):
        out = self.copy()
        out.x += offset.x
        out.y += offset.y
        return out

    def __json__(self):
        attributes = dict(vars(self))
        attributes['tags'] = list(attributes['tags'])
        return attributes

    def __getstate__(self):
        # This is used by pickle.  We want to sort the tag list so that the
        # pickled representation is stable, since it's used to generate cache
        # keys.
        state = self.__json__()
        state['tags'].sort()

        return state
