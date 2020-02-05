from copy import copy
from math import atan, degrees

from simpletransform import (applyTransformToNode, applyTransformToPoint,
                             computeBBox, parseTransform)

from ..commands import is_command
from ..i18n import _
from ..svg.path import get_node_transform
from ..svg.svg import find_elements
from ..svg.tags import (EMBROIDERABLE_TAGS, SVG_POLYLINE_TAG, SVG_USE_TAG,
                        XLINK_HREF)
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
    description = _("There is one or more clone objects in this document.  "
                    "Ink/Stitch can work with single clones, but you are limited to set a very few parameters. ")
    steps_to_solve = [
        _("If you want to convert the clone into a real element, follow these steps:"),
        _("* Select the clone"),
        _("* Run: Edit > Clone > Unlink Clone (Alt+Shift+D)")
    ]


class CloneSourceWarning(ValidationWarning):
    name = _("Clone is not embroiderable")
    description = _("There is one ore more clone objects in this document. A clone must be a direct child of an embroiderable element. "
                    "Ink/Stitch cannot embroider clones of groups or other not embroiderable elements (text or image).")
    steps_to_solve = [
        _("Convert the clone into a real element:"),
        _("* Select the clone."),
        _("* Run: Edit > Clone > Unlink Clone (Alt+Shift+D)")
    ]


class Clone(EmbroideryElement):
    # A clone embroidery element is linked to an embroiderable element.
    # It will be ignored if the source element is not a direct child of the xlink attribute.

    element_name = "Clone"

    def __init__(self, *args, **kwargs):
        super(Clone, self).__init__(*args, **kwargs)

    @property
    @param('clone_element', _("Clone"), type='toggle', inverse=False, default=True)
    def clone_element(self):
        return self.get_boolean_param("clone_element")

    @property
    @param('clone_fill_angle',
           _('Custom fill angle'),
           tooltip=_("This setting will apply a custom fill angle for the clone."),
           unit='deg',
           type='float')
    @cache
    def clone_fill_angle(self):
        return self.get_float_param("clone_fill_angle")

    def clone_to_element(self, node):
        # we need to determine if the source element is polyline, stroke, fill or satin
        element = EmbroideryElement(node)

        if node.tag == SVG_POLYLINE_TAG:
            return [Polyline(node)]

        elif element.get_boolean_param("satin_column") and element.get_style("stroke"):
            return [SatinColumn(node)]
        else:
            elements = []
            if element.get_style("fill", 'black') and not element.get_style('fill-opacity', 1) == "0":
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

    def to_patches(self, last_patch=None):
        patches = []

        source_node = get_clone_source(self.node)
        if source_node.tag not in EMBROIDERABLE_TAGS:
            return []

        clone = copy(source_node)

        # set id
        clone_id = 'clone__%s__%s' % (self.node.get('id', ''), clone.get('id', ''))
        clone.set('id', clone_id)

        # apply transform
        transform = get_node_transform(self.node)
        applyTransformToNode(transform, clone)

        # set fill angle. Use either
        # a. a custom set fill angle
        # b. calculated rotation for the cloned fill element to look exactly as it's source
        if self.clone_fill_angle is not None:
            embroider_angle = self.clone_fill_angle
        else:
            # clone angle
            clone_mat = parseTransform(clone.get('transform', ''))
            clone_angle = degrees(atan(-clone_mat[1][0]/clone_mat[1][1]))
            # source node angle
            source_mat = parseTransform(source_node.get('transform', ''))
            source_angle = degrees(atan(-source_mat[1][0]/source_mat[1][1]))
            # source node fill angle
            source_fill_angle = source_node.get('embroider_angle', 0)

            embroider_angle = clone_angle + float(source_fill_angle) - source_angle
        clone.set('embroider_angle', str(embroider_angle))

        elements = self.clone_to_element(clone)

        for element in elements:
            patches.extend(element.to_patches(last_patch))

        return patches

    def center(self, source_node):
        xmin, xmax, ymin, ymax = computeBBox([source_node])
        point = [(xmax-((xmax-xmin)/2)), (ymax-((ymax-ymin)/2))]
        transform = get_node_transform(self.node)
        applyTransformToPoint(transform, point)
        return point

    def validation_warnings(self):
        source_node = get_clone_source(self.node)
        if source_node.tag not in EMBROIDERABLE_TAGS:
            point = self.center(source_node)
            yield CloneSourceWarning(point)
        else:
            point = self.center(source_node)
            yield CloneWarning(point)


def is_clone(node):
    if node.tag == SVG_USE_TAG and node.get(XLINK_HREF) and not is_command(node):
        return True
    else:
        return False


def get_clone_source(node):
    source_id = node.get(XLINK_HREF)[1:]
    xpath = ".//*[@id='%s']" % (source_id)
    source_node = find_elements(node, xpath)[0]
    return source_node
