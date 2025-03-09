# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from __future__ import annotations  # Needed for using the Stitch type as a constructor arg
from typing import Dict, Type, Union, Optional, Set, Any, Iterable, overload
from shapely import geometry as shgeo

from ..utils.geometry import Point


class Stitch(Point):
    """A stitch is a Point with extra information telling how to sew it."""
    x: float
    y: float
    color: Any  # Todo: What is this
    jump: bool
    stop: bool
    trim: bool
    color_change: bool
    min_stitch_length: Optional[float]
    tags: Set[str]

    @overload
    def __init__(
        self,
        x: Stitch,
        color: Optional[Any] = None,
        jump=False,
        stop=False,
        trim=False,
        color_change=False,
        min_stitch_length: Optional[float] = None,
        tags: Optional[Iterable[str]] = None
    ): ...

    @overload
    def __init__(
        self,
        x: Point,
        color: Optional[Any] = None,
        jump=False,
        stop=False,
        trim=False,
        color_change=False,
        min_stitch_length: Optional[float] = None,
        tags: Optional[Iterable[str]] = None
    ): ...

    @overload
    def __init__(
        self,
        x: shgeo.Point,
        color: Optional[Any] = None,
        jump=False,
        stop=False,
        trim=False,
        color_change=False,
        min_stitch_length: Optional[float] = None,
        tags: Optional[Iterable[str]] = None
    ): ...

    @overload
    def __init__(
        self,
        x: float,
        y: float,
        color: Optional[Any] = None,
        jump: bool = False,
        stop: bool = False,
        trim: bool = False,
        color_change: bool = False,
        min_stitch_length: Optional[float] = None,
        tags: Optional[Iterable[str]] = None
    ): ...

    def __init__(
        self,
        x: Union[Stitch, float, Point],
        y: Optional[float] = None,
        color: Optional[Any] = None,
        jump: bool = False,
        stop: bool = False,
        trim: bool = False,
        color_change: bool = False,
        min_stitch_length: Optional[float] = None,
        tags: Optional[Iterable[str]] = None
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
            self.x = base_stitch.x
            self.y = base_stitch.y
        elif isinstance(x, (Point, shgeo.Point)):
            # Allow creating a Stitch from a Point
            point = x
            self.x = point.x
            self.y = point.y
        else:
            assert y is not None, "Bad stitch constructor use: No y component?"
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

    def __new__(cls: Type[Stitch], *args, **kwargs) -> Stitch:
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

    def _set(self, attribute: str, value: Optional[Any], base_stitch: Optional[Stitch]) -> None:
        # Set an attribute.  If the caller passed a Stitch object, use its value, unless
        # they overrode it with arguments.
        if base_stitch is not None:
            setattr(self, attribute, getattr(base_stitch, attribute))
        if value or base_stitch is None:
            setattr(self, attribute, value)

    @property
    def is_terminator(self) -> bool:
        return self.trim or self.stop or self.color_change

    def add_tags(self, tags: Iterable[str]) -> None:
        for tag in tags:
            self.add_tag(tag)

    def add_tag(self, tag: str) -> None:
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

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags

    def copy(self) -> Stitch:
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

    def offset(self, offset: Point) -> Stitch:
        out = self.copy()
        out.x += offset.x
        out.y += offset.y
        return out

    def __json__(self) -> Dict[str, Any]:
        attributes = dict(vars(self))
        attributes['tags'] = list(attributes['tags'])
        return attributes

    def __getstate__(self) -> Dict[str, Any]:
        # This is used by pickle.  We want to sort the tag list so that the
        # pickled representation is stable, since it's used to generate cache
        # keys.
        state = self.__json__()
        state['tags'].sort()

        return state
