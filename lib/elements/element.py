import sys
from copy import deepcopy

import inkex
import tinycss2
from inkex import bezier

from ..commands import find_commands
from ..i18n import _
from ..svg import (PIXELS_PER_MM, apply_transforms, convert_length,
                   get_node_transform)
from ..svg.tags import (EMBROIDERABLE_TAGS, INKSCAPE_LABEL, INKSTITCH_ATTRIBS,
                        SVG_GROUP_TAG, SVG_LINK_TAG, SVG_USE_TAG)
from ..utils import Point, cache


class Patch:
    """A raw collection of stitches with attached instructions."""

    def __init__(self, color=None, stitches=None, trim_after=False, stop_after=False, stitch_as_is=False):
        self.color = color
        self.stitches = stitches or []
        self.trim_after = trim_after
        self.stop_after = stop_after
        self.stitch_as_is = stitch_as_is

    def __add__(self, other):
        if isinstance(other, Patch):
            return Patch(self.color, self.stitches + other.stitches)
        else:
            raise TypeError("Patch can only be added to another Patch")

    def __len__(self):
        # This method allows `len(patch)` and `if patch:
        return len(self.stitches)

    def add_stitch(self, stitch):
        self.stitches.append(stitch)

    def reverse(self):
        return Patch(self.color, self.stitches[::-1])


class Param(object):
    def __init__(self, name, description, unit=None, values=[], type=None, group=None, inverse=False, default=None, tooltip=None, sort_index=0):
        self.name = name
        self.description = description
        self.unit = unit
        self.values = values or [""]
        self.type = type
        self.group = group
        self.inverse = inverse
        self.default = default
        self.tooltip = tooltip
        self.sort_index = sort_index

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
    def __init__(self, node):
        self.node = node

        legacy_attribs = False
        for attrib in self.node.attrib:
            if attrib.startswith('embroider_'):
                # update embroider_ attributes to namespaced attributes
                self.replace_legacy_param(attrib)
                legacy_attribs = True
        if legacy_attribs and not self.get_param('fill_underlay', ""):
            # defaut setting for fill_underlay has changed
            self.set_param('fill_underlay', False)

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
                if hasattr(prop.fget, 'param'):
                    params.append(prop.fget.param)
        return params

    def replace_legacy_param(self, param):
        value = self.node.get(param, "").strip()
        self.set_param(param[10:], value)
        del self.node.attrib[param]

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

    def set_param(self, name, value):
        param = INKSTITCH_ATTRIBS[name]
        self.node.set(param, str(value))

    @cache
    def parse_style(self, node=None):
        if node is None:
            node = self.node
        element_style = node.get("style", "")
        if element_style is None:
            return None
        declarations = tinycss2.parse_declaration_list(node.get("style", ""))
        style = {declaration.lower_name: declaration.value[0].serialize() for declaration in declarations}
        return style

    @cache
    def _get_style_raw(self, style_name):
        if self.node is None:
            return None
        if self.node.tag not in [SVG_GROUP_TAG, SVG_LINK_TAG, SVG_USE_TAG] and self.node.tag not in EMBROIDERABLE_TAGS:
            return None

        style = self.parse_style()
        if style:
            style = style.get(style_name) or self.node.get(style_name)
        parent = self.node.getparent()
        # style not found, get inherited style elements
        while not style and parent is not None:
            style = self.parse_style(parent)
            if style:
                style = style.get(style_name) or parent.get(style_name)
            parent = parent.getparent()
        return style

    def get_style(self, style_name, default=None):
        style = self._get_style_raw(style_name) or default
        if style == 'none':
            style = None
        return style

    def has_style(self, style_name):
        return self._get_style_raw(style_name) is not None

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
        zero = [0, 0]
        zero = inkex.Transform.apply_to_point(node_transform, zero)
        translate = Point(*zero)

        # Next, see how the transform affects unit vectors in the X and Y axes.  We
        # need to subtract off the translation or it will affect the magnitude of
        # the resulting vector, which we don't want.
        unit_x = [1, 0]
        unit_x = inkex.Transform.apply_to_point(node_transform, unit_x)
        sx = (Point(*unit_x) - translate).length()

        unit_y = [0, 1]
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
    @param('ties',
           _('Ties'),
           tooltip=_('Add ties. Manual stitch will not add ties.'),
           type='boolean',
           default=True,
           sort_index=4)
    @cache
    def ties(self):
        return self.get_boolean_param("ties", True)

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

        if not d:
            self.fatal(_("Object %(id)s has an empty 'd' attribute.  Please delete this object from your document.") % dict(id=self.node.get("id")))

        return inkex.paths.Path(d).to_superpath()

    @cache
    def parse_path(self):
        return apply_transforms(self.path, self.node)

    @property
    def shape(self):
        raise NotImplementedError("INTERNAL ERROR: %s must implement shape()", self.__class__)

    @property
    @cache
    def commands(self):
        return find_commands(self.node)

    @cache
    def get_commands(self, command):
        return [c for c in self.commands if c.command == command]

    @cache
    def has_command(self, command):
        return len(self.get_commands(command)) > 0

    @cache
    def get_command(self, command):
        commands = self.get_commands(command)

        if len(commands) == 1:
            return commands[0]
        elif len(commands) > 1:
            raise ValueError(_("%(id)s has more than one command of type '%(command)s' linked to it") %
                             dict(id=self.node.get(id), command=command))
        else:
            return None

    def strip_control_points(self, subpath):
        return [point for control_before, point, control_after in subpath]

    def flatten(self, path):
        """approximate a path containing beziers with a series of points"""

        path = deepcopy(path)
        bezier.cspsubdiv(path, 0.1)

        return [self.strip_control_points(subpath) for subpath in path]

    def flatten_subpath(self, subpath):
        path = [deepcopy(subpath)]
        bezier.cspsubdiv(path, 0.1)

        return self.strip_control_points(path[0])

    @property
    def trim_after(self):
        return self.get_boolean_param('trim_after', False)

    @property
    def stop_after(self):
        return self.get_boolean_param('stop_after', False)

    def to_patches(self, last_patch):
        raise NotImplementedError("%s must implement to_patches()" % self.__class__.__name__)

    def embroider(self, last_patch):
        self.validate()

        patches = self.to_patches(last_patch)

        if not self.ties:
            for patch in patches:
                patch.stitch_as_is = True

        if patches:
            patches[-1].trim_after = self.has_command("trim") or self.trim_after
            patches[-1].stop_after = self.has_command("stop") or self.stop_after

        return patches

    def fatal(self, message):
        label = self.node.get(INKSCAPE_LABEL)
        id = self.node.get("id")
        if label:
            name = "%s (%s)" % (label, id)
        else:
            name = id

        # L10N used when showing an error message to the user such as
        # "Some Path (path1234): error: satin column: One or more of the rungs doesn't intersect both rails."
        error_msg = "%s: %s %s" % (name, _("error:"), message)
        inkex.errormsg(error_msg)
        sys.exit(1)

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
            self.fatal(error.description)
