from copy import deepcopy

from simpletransform import (applyTransformToNode, composeTransform,
                             formatTransform, parseTransform)

from ..commands import is_command
from ..i18n import _
from ..svg.path import get_node_transform
from ..svg.svg import find_elements
from ..svg.tags import (EMBROIDERABLE_TAGS, SVG_GROUP_TAG, SVG_POLYLINE_TAG,
                        SVG_USE_TAG, XLINK_HREF)
from ..utils import cache
from .auto_fill import AutoFill
from .element import EmbroideryElement, param
from .fill import Fill
from .polyline import Polyline
from .satin_column import SatinColumn
from .stroke import Stroke
from .validation import ValidationWarning


class CloneWarning(ValidationWarning):
    name = _("Clone Object")
    description = _("There is one or more Clone objects in this document.  "
                    "Ink/Stitch can work with clones, but you are limited to set a very few parameters. "
                    "Also, especially for clones with a group source, it is difficult to handle the stitch path.")
    steps_to_solve = [
        _("If you want to convert the clone into a real element, follow these steps:"),
        _("Select this object."),
        _("* Do Edit > Clone > Unlink Clone (Alt+Shift+D)")
    ]


class Clone(EmbroideryElement):
    # A clone embroidery element is linked to one or more elements of other embroidery classes.

    element_name = "Clone"

    def __init__(self, *args, **kwargs):
        super(Clone, self).__init__(*args, **kwargs)

    @property
    @param('clone_element', _("Clone"), type='toggle', inverse=False, default=True)
    def clone_element(self):
        return self.get_boolean_param("clone_element")

    @property
    @param('clone_shift_fill_angle',
           _('Fill angle shifting'),
           tooltip=_("This setting will shift the fill angle in comparance to it's source element."),
           unit='deg',
           type='float')
    @cache
    def clone_shift_fill_angle(self):
        return self.get_float_param("clone_shift_fill_angle")

    def clone_to_element(self, node):
        if node.tag not in EMBROIDERABLE_TAGS:
            return []

        element = EmbroideryElement(node)

        if node.tag == SVG_POLYLINE_TAG:
            return [Polyline(node)]

        elif element.get_boolean_param("satin_column") and element.get_style("stroke"):
            return [SatinColumn(node)]
        else:
            elements = []

            if element.get_style("fill", "black"):
                if element.get_boolean_param("auto_fill", True):
                    elements.append(AutoFill(node))
                else:
                    elements.append(Fill(node))

            if element.get_style("stroke"):
                if not is_command(element.node):
                    elements.append(Stroke(node))

            if element.get_boolean_param("stroke_first", False):
                elements.reverse()

            return elements

    def clones_to_elements(self, node, trans=''):
        elements = []

        source_node = get_clone_source(node)
        clone = deepcopy(source_node)

        if trans:
            transform = parseTransform(trans)
        else:
            transform = get_node_transform(node)
        applyTransformToNode(transform, clone)

        if is_clone(source_node):
            elements.extend(self.clones_to_elements(source_node, clone.get('transform')))

        else:
            if clone.tag == SVG_GROUP_TAG:

                for clone_node in clone.iterdescendants():
                    if is_clone(clone_node):
                        clone_node_source = get_clone_source(node, clone_node.get('id'))
                        transform = formatTransform(composeTransform(transform, parseTransform(clone_node_source.get('transform'))))
                        elements.extend(self.clones_to_elements(clone_node_source, transform))

                    clone_id = 'clones__%s__%s' % (node.get('id', ''), clone_node.get('id', ''))
                    clone_node.set('id', clone_id)
                    if self.clone_shift_fill_angle:
                        clone_node.set('embroider_angle', self.get_fill_angle(clone_node))

                    elements.extend(self.clone_to_element(clone_node))
            else:
                clone_id = 'clone__%s__%s' % (node.get('id', ''), clone.get('id', ''))
                clone.set('id', clone_id)
                if self.clone_shift_fill_angle:
                    clone.set('embroider_angle', self.get_fill_angle(clone))
                elements.extend(self.clone_to_element(clone))

        return elements

    def get_fill_angle(self, clone):
        clone_fill_angle = float(clone.get('embroider_angle', 0)) + self.clone_shift_fill_angle
        return str(clone_fill_angle)

    def to_patches(self, last_patch=None):
        patches = []
        elements = self.clones_to_elements(self.node)

        for element in elements:
            patches.extend(element.to_patches(last_patch))

        return patches

    def validation_warnings(self):
        # This will always point to (0,0), which is not ideal - but for a lazy reason.
        # We would need to go through every cloned element with an uncertain type of source.
        # So, let's be lazy here and just tell the user how to unlink clones in the description.
        point = [float(self.node.get('x', '')), float(self.node.get('y', ''))]
        yield CloneWarning(point)


def is_clone(node):
    if not node.tag == SVG_USE_TAG or (node.tag == SVG_USE_TAG and is_command(node)):
        return False

    elif node.tag == SVG_USE_TAG and node.get(XLINK_HREF, ''):
        return True


def get_clone_source(node, id=None):
    if not id:
        orig_id = node.get(XLINK_HREF)[1:]
    else:
        orig_id = id
    xpath = ".//*[@id='%s']" % (orig_id)
    source_node = find_elements(node, xpath)[0]
    return source_node
