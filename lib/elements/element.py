# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
from __future__ import annotations

import json
import sys
from contextlib import contextmanager
from copy import deepcopy
from typing import List, Optional

import inkex
import numpy as np
from inkex import BaseElement, Color, bezier
from shapely import Point as ShapelyPoint
from shapely.ops import nearest_points

from ..commands import Command, find_commands
from ..debug.debug import debug
from ..exceptions import InkstitchException, format_uncaught_exception
from ..i18n import _
from ..marker import get_marker_elements_cache_key_data
from ..patterns import apply_patterns, get_patterns_cache_key_data
from ..stitch_plan import StitchGroup
from ..stitch_plan.lock_stitch import (LOCK_DEFAULTS, AbsoluteLock, CustomLock,
                                       LockStitch, SVGLock)
from ..svg import (PIXELS_PER_MM, apply_transforms, convert_length,
                   get_node_transform)
from ..svg.clip import get_clip_path
from ..svg.tags import INKSCAPE_LABEL, INKSTITCH_ATTRIBS
from ..utils import DotDict, Point, cache
from ..utils.cache import (CacheKeyGenerator, get_stitch_plan_cache,
                           is_cache_disabled)


class Param(object):
    def __init__(self, name, description, unit=None, values=[], type=None, group=None, inverse=False,
                 options=[], default=None, tooltip=None, sort_index=0, select_items=None, enables=None):
        self.name = name
        self.description = description
        self.unit = unit
        self.values = values or [""]
        self.type = type
        self.group = group
        self.inverse = inverse
        self.options = options
        self.default = default
        self.tooltip = tooltip
        self.sort_index = sort_index
        self.select_items = select_items
        self.enables = enables

    def __repr__(self):
        return "Param(%s)" % vars(self)


# Decorate a member function or property with information about
# the embroidery parameter it corresponds to
def param(*args, **kwargs):
    p = Param(*args, **kwargs)

    def decorator(func):
        func.param = p
        return func

    return decorator


class EmbroideryElement(object):
    def __init__(self, node: BaseElement):
        self.node = node

    @property
    def id(self):
        return self.node.get('id')

    @classmethod
    def get_params(cls):
        params = []
        for attr in dir(cls):
            prop = getattr(cls, attr)
            if isinstance(prop, property):
                # The 'param' attribute is set by the 'param' decorator defined above.
                fget = prop.fget
                if fget is not None and hasattr(fget, 'param'):
                    params.append(fget.param)
        return params

    @cache
    def get_param(self, param, default):
        value = self.node.get(INKSTITCH_ATTRIBS[param], "").strip()
        return value or default

    @cache
    def get_boolean_param(self, param, default=None):
        value = self.get_param(param, default)

        if isinstance(value, bool):
            return value
        else:
            return value and (value.lower() in ('yes', 'y', 'true', 't', '1'))

    @cache
    def get_float_param(self, param, default=None):
        try:
            value = float(self.get_param(param, default))
        except (TypeError, ValueError):
            value = default

        if value is None:
            return value

        if param.endswith('_mm'):
            value = value * PIXELS_PER_MM

        return value

    @cache
    def get_int_param(self, param, default=None):
        try:
            value = int(self.get_param(param, default))
        except (TypeError, ValueError):
            return default

        if param.endswith('_mm'):
            value = int(value * PIXELS_PER_MM)

        return value

    # returns 2 float values as a numpy array
    # if a single number is given in the param, it will apply to both returned values.
    # Not cached the cache will crash if the default is a numpy array.
    # The ppoperty calling this will need to cache itself and can safely do so since it has no parameters
    def get_split_float_param(self, param, default=(0, 0)):
        default = np.array(default)  # type coersion in case the default is a tuple

        raw = self.get_param(param, "")
        parts = raw.split()
        try:
            if len(parts) == 0:
                return default
            elif len(parts) == 1:
                a = float(parts[0])
                return np.array([a, a])
            else:
                a = float(parts[0])
                b = float(parts[1])
                return np.array([a, b])
        except (TypeError, ValueError):
            return default

    # not cached
    def get_split_mm_param_as_px(self, param, default):
        return self.get_split_float_param(param, default) * PIXELS_PER_MM

    # returns an array of multiple space separated int values
    @cache
    def get_multiple_int_param(self, param, default="0"):
        params = self.get_param(param, default).split(" ")
        try:
            params = [int(param) for param in params if param]
        except (TypeError, ValueError):
            return [int(default)]
        return params

    # returns an array of multiple space separated float values
    @cache
    def get_multiple_float_param(self, param, default="0"):
        params = self.get_param(param, default).split(" ")
        try:
            params = [float(param) for param in params if param]
        except (TypeError, ValueError):
            return [float(default)]
        return params

    def get_json_param(self, param, default=None):
        json_value = self.get_param(param, None)
        try:
            return json.loads(json_value, object_hook=DotDict)
        except (json.JSONDecodeError, TypeError):
            if default is None:
                return DotDict()
            else:
                return DotDict(default)

    def set_json_param(self, param, value):
        json_value = json.dumps(value)
        self.set_param(param, json_value)

    def set_param(self, name, value):
        # Sets a param on the node backing this element. Used by params dialog.
        # After calling, this element is invalid due to caching and must be re-created to use the new value.
        param = INKSTITCH_ATTRIBS[name]
        self.node.set(param, str(value))

    def remove_param(self, name):
        param = INKSTITCH_ATTRIBS[name]
        del self.node.attrib[param]

    @cache
    def _get_specified_style(self):
        # We want to cache this, because it's quite expensive to generate.
        return self.node.specified_style()

    def get_style(self, style_name, default=None):
        element_style = self._get_specified_style()
        style = element_style.get(style_name, default)
        if style in ['none', 'None']:
            style = None
        return style

    def _get_color(self, node, color_location, default=None):
        try:
            color = node.get_computed_style(color_location)
            if isinstance(color, inkex.LinearGradient) and len(color.stops) == 1:
                # Inkscape swatches set as a linear gradient with only one stop color
                # Ink/Stitch should render the color correctly
                color = self._get_color(color.stops[0], "stop-color", default)
        except (inkex.ColorError, ValueError):
            # A color error could show up, when an element has an unrecognized color name
            # A value error could show up, when for example when an element links to a non-existent gradient
            # TODO: This will also apply to currentcolor and alike which will not render
            color = default
        return color

    @property
    @cache
    def fill_color(self):
        return self._get_color(self.node, "fill", "black")

    @property
    @cache
    def stroke_color(self):
        return self._get_color(self.node, "stroke")

    @property
    @cache
    def stroke_scale(self):
        # How wide is the stroke, after the transforms are applied?
        #
        # If the transform is just simple scaling that preserves the aspect ratio,
        # then this is completely accurate.  If there's uneven scaling or skewing,
        # then the stroke is bent out of shape.  We'll make an approximation based on
        # the average scaling in the X and Y axes.
        #
        # Of course, transforms may also involve rotation, skewing, and translation.
        # All except translation can affect how wide the stroke appears on the screen.

        node_transform = inkex.transforms.Transform(get_node_transform(self.node))

        # First, figure out the translation component of the transform.  Using a zero
        # vector completely cancels out the rotation, scale, and skew components.
        zero = (0, 0)
        zero = inkex.Transform.apply_to_point(node_transform, zero)
        translate = Point(*zero)

        # Next, see how the transform affects unit vectors in the X and Y axes.  We
        # need to subtract off the translation or it will affect the magnitude of
        # the resulting vector, which we don't want.
        unit_x = (1, 0)
        unit_x = inkex.Transform.apply_to_point(node_transform, unit_x)
        sx = (Point(*unit_x) - translate).length()

        unit_y = (0, 1)
        unit_y = inkex.Transform.apply_to_point(node_transform, unit_y)
        sy = (Point(*unit_y) - translate).length()

        # Take the average as a best guess.
        node_scale = (sx + sy) / 2.0

        return node_scale

    @property
    @cache
    def stroke_width(self):
        width = self.get_style("stroke-width", "1.0")
        width = convert_length(width)
        return width * self.stroke_scale

    @property
    @param('min_stitch_length_mm',
           _('Minimum stitch length'),
           tooltip=_('Overwrite global minimum stitch length setting. Shorter stitches than that will be removed.'),
           type='float',
           default=None,
           sort_index=200)
    @cache
    def min_stitch_length(self):
        return self.get_float_param("min_stitch_length_mm")

    @property
    @param('min_jump_stitch_length_mm',
           _('Minimum jump stitch length'),
           tooltip=_('Overwrite global minimum jump stitch length setting. Shorter distances to the next object will have no lock stitches.'),
           type='float',
           default=None,
           sort_index=201)
    @cache
    def min_jump_stitch_length(self):
        return self.get_float_param("min_jump_stitch_length_mm")

    @property
    @param('ties',
           _('Allow lock stitches'),
           tooltip=_('Tie thread at the beginning and/or end of this object. '
                     'Manual stitch will only add lock stitches if force lock stitched is checked.'),
           type='dropdown',
           # Ties: 0 = Both | 1 = Before | 2 = After | 3 = Neither
           # L10N options to allow lock stitch before and after objects
           options=[_("Both"), _("Before"), _("After"), _("Neither")],
           default=0,
           sort_index=202)
    @cache
    def ties(self):
        return self.get_int_param("ties", 0)

    @property
    @param('force_lock_stitches',
           _('Force lock stitches'),
           tooltip=_('Sew lock stitches after sewing this element, '
                     'even if the distance to the next object is shorter than defined by the '
                     'minimum jump stitch length value in the Ink/Stitch preferences.'),
           type='boolean',
           default=False,
           sort_index=203)
    @cache
    def force_lock_stitches(self):
        return self.get_boolean_param('force_lock_stitches', False)

    @property
    @param('lock_start',
           _('Tack stitch'),
           tooltip=_('Tack down stitch type'),
           type='combo',
           default='half_stitch',
           options=LOCK_DEFAULTS['start'],
           sort_index=204)
    def lock_start(self):
        return self.get_param('lock_start', "half_stitch")

    @property
    @param('lock_custom_start',
           _('Custom path'),
           tooltip=_("Enter a custom path. For svg paths The last node will not be embroidered, but represents the first stitch of the element."),
           type="string",
           default="",
           select_items=[('lock_start', 'custom')],
           sort_index=205)
    def lock_custom_start(self):
        return self.get_param('lock_custom_start', '')

    @property
    @param('lock_start_scale_mm',
           _('Scale tack stitch'),
           tooltip=_('Set stitch length. A 1 in a custom path equals this values.'),
           type='float',
           unit="mm",
           default=0.7,
           select_items=[('lock_start', lock.id) for lock in LOCK_DEFAULTS['start'] if isinstance(lock, (AbsoluteLock, CustomLock))],
           sort_index=206)
    def lock_start_scale_mm(self):
        return self.get_float_param('lock_start_scale_mm', 0.7)

    @property
    @param('lock_start_scale_percent',
           _('Scale tack stitch'),
           tooltip=_('Scale tack stitch by this percentage.'),
           type='float',
           unit="%",
           default=100,
           select_items=[('lock_start', lock.id) for lock in LOCK_DEFAULTS['start'] if isinstance(lock, (SVGLock, CustomLock))],
           sort_index=207)
    def lock_start_scale_percent(self):
        return self.get_float_param('lock_start_scale_percent', 100)

    @property
    @param('lock_end',
           _('Lock stitch'),
           tooltip=_('Lock stitch type'),
           type='combo',
           default='half_stitch',
           options=LOCK_DEFAULTS['end'],
           sort_index=208)
    def lock_end(self):
        return self.get_param('lock_end', "half_stitch")

    @property
    @param('lock_custom_end',
           _('Custom path'),
           tooltip=_("Enter a custom path. For svg paths the first node will not be embroidered, but represents the last stitch of the element."),
           type="string",
           default="",
           select_items=[('lock_end', 'custom')],
           sort_index=209)
    def lock_custom_end(self):
        return self.get_param('lock_custom_end', '')

    @property
    @param('lock_end_scale_mm',
           _('Scale lock stitch'),
           tooltip=_('Set length of lock stitches (mm).'),
           type='float',
           unit="mm",
           default=0.7,
           select_items=[('lock_end', lock.id) for lock in LOCK_DEFAULTS['end'] if isinstance(lock, (AbsoluteLock, CustomLock))],
           sort_index=210)
    def lock_end_scale_mm(self):
        return self.get_float_param('lock_end_scale_mm', 0.7)

    @property
    @param('lock_end_scale_percent',
           _('Scale lock stitch'),
           tooltip=_('Scale lock stitch by this percentage.'),
           type='float',
           unit="%",
           default=100,
           select_items=[('lock_end', lock.id) for lock in LOCK_DEFAULTS['end'] if isinstance(lock, (SVGLock, CustomLock))],
           sort_index=211)
    @cache
    def lock_end_scale_percent(self):
        return self.get_float_param('lock_end_scale_percent', 100)

    @property
    @param('trim_after',
           _('Trim After'),
           tooltip=_('Add a TRIM command after stitching this object.'),
           type='boolean',
           default=False,
           sort_index=212)
    def trim_after(self):
        return self.get_boolean_param('trim_after', False)

    @property
    @param('stop_after',
           _('Stop After'),
           tooltip=_('Add a STOP command after stitching this object.'),
           type='boolean',
           default=False,
           sort_index=213)
    def stop_after(self):
        return self.get_boolean_param('stop_after', False)

    @property
    def path(self):
        # A CSP is a  "cubic superpath".
        #
        # A "path" is a sequence of strung-together bezier curves.
        #
        # A "superpath" is a collection of paths that are all in one object.
        #
        # The "cubic" bit in "cubic superpath" is because the bezier curves
        # inkscape uses involve cubic polynomials.
        #
        # Each path is a collection of tuples, each of the form:
        #
        # (control_before, point, control_after)
        #
        # A bezier curve segment is defined by an endpoint, a control point,
        # a second control point, and a final endpoint.  A path is a bunch of
        # bezier curves strung together.  One could represent a path as a set
        # of four-tuples, but there would be redundancy because the ending
        # point of one bezier is the starting point of the next.  Instead, a
        # path is a set of 3-tuples as shown above, and one must construct
        # each bezier curve by taking the appropriate endpoints and control
        # points.  Bleh. It should be noted that a straight segment is
        # represented by having the control point on each end equal to that
        # end's point.
        #
        # In a path, each element in the 3-tuple is itself a tuple of (x, y).
        # Tuples all the way down.  Hasn't anyone heard of using classes?

        if getattr(self.node, "get_path", None):
            d = self.node.get_path()
        else:
            d = self.node.get("d", "")

        return inkex.Path(d).to_superpath()

    @property
    def is_closed_path(self):
        return isinstance(self.node.get_path()[-1], inkex.paths.ZoneClose)

    @cache
    def parse_path(self):
        return apply_transforms(self.path, self.node)

    @property
    @cache
    def paths(self):
        return self.flatten(self.parse_path())

    @property
    def shape(self):
        raise NotImplementedError("INTERNAL ERROR: %s must implement shape()", self.__class__)

    @property
    def first_stitch(self) -> Optional[ShapelyPoint]:
        # first stitch is an approximation to where the first stitch may possibly be
        # if not defined through commands or repositioned by the previous element
        raise NotImplementedError("INTERNAL ERROR: %s must implement first_stitch()", self.__class__)

    @property
    @cache
    def commands(self) -> List[Command]:
        return find_commands(self.node)

    @cache
    def get_commands(self, command: str) -> List[Command]:
        return [c for c in self.commands if c.command == command]

    @cache
    def has_command(self, command: str) -> bool:
        return len(self.get_commands(command)) > 0

    @cache
    def get_command(self, command: str, multiple: bool = False) -> Optional[Command]:
        commands = self.get_commands(command)

        if commands:
            if multiple:
                return commands
            else:
                return commands[0]
        else:
            return None

    def strip_control_points(self, subpath):
        return [point for control_before, point, control_after in subpath]

    def flatten(self, path):
        """approximate a path containing beziers with a series of points"""

        path = deepcopy(path)
        bezier.cspsubdiv(path, 0.1)

        return [self.strip_control_points(subpath) for subpath in path]

    @property
    @cache
    def lock_stitches(self):
        lock_start = None
        lock_end = None

        # Ties: 0 = Both | 1 = Before | 2 = After | 3 = Neither
        tie_modus = self.ties
        force = self.force_lock_stitches

        if tie_modus in [0, 1]:
            lock_start = LockStitch('start', self.lock_start, scale_percent=self.lock_start_scale_percent, scale_absolute=self.lock_start_scale_mm)
            if self.lock_start == "custom":
                lock_start.set_path(self.lock_custom_start)

        if tie_modus in [0, 2] or force:
            lock_end = LockStitch('end', self.lock_end, scale_percent=self.lock_end_scale_percent, scale_absolute=self.lock_end_scale_mm)
            if self.lock_end == "custom":
                lock_end.set_path(self.lock_custom_end)

        return lock_start, lock_end

    def to_stitch_groups(self, last_stitch_group: Optional[StitchGroup], next_element: Optional[EmbroideryElement] = None) -> List[StitchGroup]:
        raise NotImplementedError("%s must implement to_stitch_groups()" % self.__class__.__name__)

    @debug.time
    def _load_cached_stitch_groups(self, previous_stitch, next_element):
        if is_cache_disabled():
            return None

        if not self.uses_previous_stitch():
            # we don't care about the previous stitch
            previous_stitch = None

        cache_key = self.get_cache_key(previous_stitch, next_element)
        stitch_groups = get_stitch_plan_cache().get(cache_key)

        if stitch_groups:
            debug.log(f"used cache for {self.node.get('id')} {self.node.get(INKSCAPE_LABEL)}")
        else:
            debug.log(f"did not use cache for {self.node.get('id')} {self.node.get(INKSCAPE_LABEL)}, key={cache_key}")

        return stitch_groups

    def uses_previous_stitch(self) -> bool:
        """Returns True if the previous stitch can affect this Element's stitches.

        This function may be overridden in a subclass.
        """
        return False

    def uses_next_element(self) -> bool:
        """Returns True if the shape of the next element can affect this Element's stitches.

        This function may be overridden in a subclass.
        """
        return False

    @debug.time
    def _save_cached_stitch_groups(self, stitch_groups, previous_stitch, next_element):
        if is_cache_disabled():
            return

        stitch_plan_cache = get_stitch_plan_cache()
        cache_key = self.get_cache_key(previous_stitch, next_element)
        if cache_key not in stitch_plan_cache:
            # fix up colors for cache
            for stitch_group in stitch_groups:
                if not isinstance(stitch_group.color, Color):
                    stitch_group.color = "black"
            stitch_plan_cache[cache_key] = stitch_groups

        if previous_stitch is not None:
            # Also store it with None as the previous stitch, so that it can be used next time
            # if we don't care about the previous stitch
            cache_key = self.get_cache_key(None, None)
            if cache_key not in stitch_plan_cache:
                stitch_plan_cache[cache_key] = stitch_groups

    def get_params_and_values(self):
        params = {}
        for param in self.get_params():
            params[param.name] = self.get_param(param.name, param.default)

        return params

    @cache
    def _get_patterns_cache_key_data(self):
        return get_patterns_cache_key_data(self.node)

    @cache
    def _get_guides_cache_key_data(self):
        return get_marker_elements_cache_key_data(self.node, "guide-line")

    @cache
    def _get_ripple_cache_key_data(self):
        return get_marker_elements_cache_key_data(self.node, "anchor-line")

    def _get_gradient_cache_key_data(self):
        gradient = {}
        if hasattr(self, 'gradient') and self.gradient is not None:
            # prevent issue with color parsing: https://github.com/inkstitch/inkstitch/issues/3742
            try:
                gradient['stops'] = self.gradient.stop_offsets
                gradient['orientation'] = [self.gradient.x1(), self.gradient.x2(), self.gradient.y1(), self.gradient.y2()]
                gradient['styles'] = [(stop.style('stop-color'), stop.style('stop-opacity')) for stop in self.gradient.stops]
            except ValueError:
                pass
        return gradient

    def _get_tartan_key_data(self):
        return (self.node.get('inkstitch:tartan', None))

    def get_cache_key_data(self, previous_stitch, next_element):
        return []

    def get_cache_key(self, previous_stitch, next_element):
        cache_key_generator = CacheKeyGenerator()
        cache_key_generator.update(self.__class__.__name__)
        cache_key_generator.update(self.get_params_and_values())
        cache_key_generator.update(self.parse_path())
        cache_key_generator.update(self.clip_shape)
        cache_key_generator.update(list(self._get_specified_style().items()))
        cache_key_generator.update(self._get_gradient_cache_key_data())
        cache_key_generator.update(previous_stitch)
        if next_element is not None:
            cache_key_generator.update(next_element.get_cache_key(None, None))
        cache_key_generator.update([(c.command, c.target_point) for c in self.commands])
        cache_key_generator.update(self._get_patterns_cache_key_data())
        cache_key_generator.update(self._get_guides_cache_key_data())
        cache_key_generator.update(self._get_ripple_cache_key_data())
        cache_key_generator.update(self.get_cache_key_data(previous_stitch, next_element))
        cache_key_generator.update(self._get_tartan_key_data())

        cache_key = cache_key_generator.get_cache_key()
        debug.log(f"cache key for {self.node.get('id')} {self.node.get(INKSCAPE_LABEL)} {previous_stitch} {next_element}: {cache_key}")

        return cache_key

    def embroider(self, last_stitch_group: Optional[StitchGroup], next_element=None) -> List[StitchGroup]:
        debug.log(f"starting {self.node.get('id')} {self.node.get(INKSCAPE_LABEL)}")

        with self.handle_unexpected_exceptions():
            if last_stitch_group:
                previous_stitch = last_stitch_group.stitches[-1]
            else:
                previous_stitch = None

            stitch_groups = self._load_cached_stitch_groups(previous_stitch, next_element)

            if not stitch_groups:
                self.validate()

                stitch_groups = self.to_stitch_groups(last_stitch_group, next_element)
                apply_patterns(stitch_groups, self.node)

                if stitch_groups:
                    # In some cases (clones) the last stitch group may have trim_after or stop_after already set,
                    # and we shouldn't override that with this element's values, hence the use of or-equals
                    stitch_groups[-1].trim_after |= self.has_command("trim") or self.trim_after
                    stitch_groups[-1].stop_after |= self.has_command("stop") or self.stop_after

                for stitch_group in stitch_groups:
                    stitch_group.min_jump_stitch_length = self.min_jump_stitch_length
                    stitch_group.set_minimum_stitch_length(self.min_stitch_length)

                self._save_cached_stitch_groups(stitch_groups, previous_stitch, next_element)

        debug.log(f"ending {self.node.get('id')} {self.node.get(INKSCAPE_LABEL)}")
        return stitch_groups

    def next_stitch(self, next_element):
        next_stitch = None
        if next_element is not None and self.uses_next_element():
            # in fact we really only try an approximation to the next stitch
            if next_element.uses_previous_stitch():
                try:
                    next_stitch = nearest_points(next_element.shape, self.shape)[1]
                except (ValueError, AttributeError):
                    pass
            else:
                try:
                    next_stitch = nearest_points(next_element.first_stitch, self.shape)[1]
                except (ValueError, AttributeError):
                    pass
        return next_stitch

    @property
    @cache
    def clip_shape(self):
        return get_clip_path(self.node)

    def fatal(self, message, point_to_troubleshoot=False):
        label = self.node.get(INKSCAPE_LABEL)
        id = self.node.get("id")
        if label:
            name = "%s (%s)" % (label, id)
        else:
            name = id

        error_msg = f"{name}: {message}"
        if point_to_troubleshoot:
            error_msg += "\n\n%s" % _("Please run Extensions > Ink/Stitch > Troubleshoot > Troubleshoot objects. "
                                      "This will show you the exact location of the problem.")

        raise InkstitchException(error_msg)

    @contextmanager
    def handle_unexpected_exceptions(self):
        try:
            # This runs the code in the `with` body so that we can catch
            # exceptions.
            yield
        except (InkstitchException, SystemExit, KeyboardInterrupt):
            raise
        except Exception:
            if hasattr(sys, 'gettrace') and sys.gettrace():
                # if we're debugging, let the exception bubble up
                raise

            raise InkstitchException(format_uncaught_exception())

    def validation_errors(self):
        """Return a list of errors with this Element.

        Validation errors will prevent the Element from being stitched.

        Return value: an iterable or generator of instances of subclasses of ValidationError
        """
        return []

    def validation_warnings(self):
        """Return a list of warnings about this Element.

        Validation warnings don't prevent the Element from being stitched but
        the user should probably fix them anyway.

        Return value: an iterable or generator of instances of subclasses of ValidationWarning
        """
        return []

    def is_valid(self):
        # We have to iterate since it could be a generator.
        for error in self.validation_errors():
            return False

        return True

    def validate(self):
        """Print an error message and exit if this Element is invalid."""

        for error in self.validation_errors():
            # note that self.fatal() exits, so this only shows the first error
            self.fatal(error.description, True)
