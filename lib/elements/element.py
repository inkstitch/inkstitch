from copy import deepcopy
import sys

from cspsubdiv import cspsubdiv
import cubicsuperpath
import simplestyle

from ..commands import find_commands
from ..i18n import _
from ..svg import PIXELS_PER_MM, apply_transforms, convert_length, get_doc_size
from ..svg.tags import INKSCAPE_LABEL
from ..utils import cache


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

    @cache
    def get_param(self, param, default):
        value = self.node.get("embroider_" + param, "").strip()

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
        self.node.set("embroider_%s" % name, str(value))

    @cache
    def get_style(self, style_name, default=None):
        style = simplestyle.parseStyle(self.node.get("style"))
        if (style_name not in style):
            return default
        value = style[style_name]
        if value == 'none':
            return None
        return value

    @cache
    def has_style(self, style_name):
        style = simplestyle.parseStyle(self.node.get("style"))
        return style_name in style

    @property
    @cache
    def stroke_scale(self):
        svg = self.node.getroottree().getroot()
        doc_width, doc_height = get_doc_size(svg)
        viewbox = svg.get('viewBox', '0 0 %s %s' % (doc_width, doc_height))
        viewbox = viewbox.strip().replace(',', ' ').split()
        return doc_width / float(viewbox[2])

    @property
    @cache
    def stroke_width(self):
        width = self.get_style("stroke-width", "1")

        if width is None:
            return 1.0

        width = convert_length(width)
        return width * self.stroke_scale

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

        d = self.node.get("d", "")
        if not d:
            self.fatal(_("Object %(id)s has an empty 'd' attribute.  Please delete this object from your document.") % dict(id=self.node.get("id")))

        return cubicsuperpath.parsePath(d)

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
        cspsubdiv(path, 0.1)

        return [self.strip_control_points(subpath) for subpath in path]

    def flatten_subpath(self, subpath):
        path = [deepcopy(subpath)]
        cspsubdiv(path, 0.1)

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
        print >> sys.stderr, "%s" % (error_msg.encode("UTF-8"))
        sys.exit(1)

    def validation_errors(self):
        """Return a list of problems with this Element.

        Return value: an iterable or generator of tuples (message, location)

          message - a description of a problem
          location - coordinates of the problem, or None for general problems
        """
        raise NotImplementedError("Element subclass is expected to implement method: validation_errors")

    def is_valid(self):
        # We have to iterate since it could be a generator.
        for message, location in self.validation_errors():
            return False

        return True

    def validate(self):
        """Print an error message and exit if this Element is invalid."""

        for message, location in self.validation_errors():
            # note that self.fatal() exits, so this only shows the first error
            self.fatal(message)
