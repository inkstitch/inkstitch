import sys
from copy import deepcopy

from ..utils import cache
from shapely import geometry as shgeo
from .. import _, PIXELS_PER_MM, get_viewbox_transform, get_stroke_scale, convert_length

# inkscape-provided utilities
import simpletransform
import simplestyle
import cubicsuperpath
from cspsubdiv import cspsubdiv

class Patch:
    """A raw collection of stitches with attached instructions."""

    def __init__(self, color=None, stitches=None, trim_after=False, stop_after=False):
        self.color = color
        self.stitches = stitches or []
        self.trim_after = trim_after
        self.stop_after = stop_after

    def __add__(self, other):
        if isinstance(other, Patch):
            return Patch(self.color, self.stitches + other.stitches)
        else:
            raise TypeError("Patch can only be added to another Patch")

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
            return default

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
    def get_style(self, style_name):
        style = simplestyle.parseStyle(self.node.get("style"))
        if (style_name not in style):
            return None
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
    def stroke_width(self):
        width = self.get_style("stroke-width")

        if width is None:
            return 1.0

        width = convert_length(width)

        return width * get_stroke_scale(self.node.getroottree().getroot())

    @property
    def path(self):
        return cubicsuperpath.parsePath(self.node.get("d"))

    @cache
    def parse_path(self):
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

        path = self.path

        # start with the identity transform
        transform = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]

        # combine this node's transform with all parent groups' transforms
        transform = simpletransform.composeParents(self.node, transform)

        # add in the transform implied by the viewBox
        viewbox_transform = get_viewbox_transform(self.node.getroottree().getroot())
        transform = simpletransform.composeTransform(viewbox_transform, transform)

        # apply the combined transform to this node's path
        simpletransform.applyTransformToPath(transform, path)


        return path

    def flatten(self, path):
        """approximate a path containing beziers with a series of points"""

        path = deepcopy(path)

        cspsubdiv(path, 0.1)

        flattened = []

        for comp in path:
            vertices = []
            for ctl in comp:
                vertices.append((ctl[1][0], ctl[1][1]))
            flattened.append(vertices)

        return flattened

    @property
    @param('trim_after',
           _('TRIM after'),
           tooltip=_('Trim thread after this object (for supported machines and file formats)'),
           type='boolean',
           default=False,
           sort_index=1000)
    def trim_after(self):
        return self.get_boolean_param('trim_after', False)

    @property
    @param('stop_after',
           _('STOP after'),
           tooltip=_('Add STOP instruction after this object (for supported machines and file formats)'),
           type='boolean',
           default=False,
           sort_index=1000)
    def stop_after(self):
        return self.get_boolean_param('stop_after', False)

    def to_patches(self, last_patch):
        raise NotImplementedError("%s must implement to_patches()" % self.__class__.__name__)

    def embroider(self, last_patch):
        patches = self.to_patches(last_patch)

        if patches:
            patches[-1].trim_after = self.trim_after
            patches[-1].stop_after = self.stop_after

        return patches

    def fatal(self, message):
        print >> sys.stderr, "error:", message
        sys.exit(1)
