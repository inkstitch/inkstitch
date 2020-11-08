from math import atan, degrees

import inkex

from ..commands import is_command, is_command_symbol
from ..i18n import _
from ..svg.path import get_node_transform
from ..svg.svg import find_elements
from ..svg.tags import (EMBROIDERABLE_TAGS, INKSTITCH_ATTRIBS,
                        SVG_POLYLINE_TAG, SVG_USE_TAG, XLINK_HREF)
from ..utils import cache
from .auto_fill import AutoFill
from .element import EmbroideryElement, param
from .fill import Fill
from .polyline import Polyline
from .satin_column import SatinColumn
from .stroke import Stroke
from .validation import ObjectTypeWarning, ValidationWarning


class CloneWarning(ValidationWarning):
    name = _("Clone Object")
    description = _("There are one or more clone objects in this document.  "
                    "Ink/Stitch can work with single clones, but you are limited to set a very few parameters. ")
    steps_to_solve = [
        _("If you want to convert the clone into a real element, follow these steps:"),
        _("* Select the clone"),
        _("* Run: Edit > Clone > Unlink Clone (Alt+Shift+D)")
    ]


class CloneSourceWarning(ObjectTypeWarning):
    name = _("Clone is not embroiderable")
    description = _("There are one ore more clone objects in this document. A clone must be a direct child of an embroiderable element. "
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
    @param('clone', _("Clone"), type='toggle', inverse=False, default=True)
    def clone(self):
        return self.get_boolean_param("clone")

    @property
    @param('angle',
           _('Custom fill angle'),
           tooltip=_("This setting will apply a custom fill angle for the clone."),
           unit='deg',
           type='float')
    @cache
    def clone_fill_angle(self):
        return self.get_float_param('angle', 0)

    def clone_to_element(self, node):
        # we need to determine if the source element is polyline, stroke, fill or satin
        element = EmbroideryElement(node)

        if node.tag == SVG_POLYLINE_TAG:
            return [Polyline(node)]

        elif element.get_boolean_param("satin_column") and self.get_clone_style("stroke", self.node):
            return [SatinColumn(node)]
        else:
            elements = []
            if element.get_style("fill", "black") and not element.get_style("stroke", 1) == "0":
                if element.get_boolean_param("auto_fill", True):
                    elements.append(AutoFill(node))
                else:
                    elements.append(Fill(node))
            if element.get_style("stroke", self.node) is not None:
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

        self.node.style = source_node.composed_style()

        # a. a custom set fill angle
        # b. calculated rotation for the cloned fill element to look exactly as it's source
        param = INKSTITCH_ATTRIBS['angle']
        if self.clone_fill_angle is not None:
            angle = self.clone_fill_angle
        else:
            # clone angle
            clone_mat = self.node.composed_transform()
            clone_angle = degrees(atan(-clone_mat[1][0]/clone_mat[1][1]))
            # source node angle
            source_mat = source_node.composed_transform()
            source_angle = degrees(atan(-source_mat[1][0]/source_mat[1][1]))
            # source node fill angle
            source_fill_angle = source_node.get(param, 0)

            angle = clone_angle + float(source_fill_angle) - source_angle
        self.node.set(param, str(angle))

        elements = self.clone_to_element(self.node)

        for element in elements:
            patches.extend(element.to_patches(last_patch))

        return patches

    def get_clone_style(self, style_name, node, default=None):
        style = inkex.styles.AttrFallbackStyle(node).get(style_name) or default
        return style

    def center(self, source_node):
        transform = get_node_transform(self.node.getparent())
        center = self.node.bounding_box(transform).center
        return center

    def validation_warnings(self):
        source_node = get_clone_source(self.node)
        if source_node.tag not in EMBROIDERABLE_TAGS:
            point = self.center(source_node)
            yield CloneSourceWarning(point)
        else:
            point = self.center(source_node)
            yield CloneWarning(point)


def is_clone(node):
    if node.tag == SVG_USE_TAG and node.get(XLINK_HREF) and not is_command_symbol(node):
        return True
    return False


def is_embroiderable_clone(node):
    if is_clone(node) and get_clone_source(node).tag in EMBROIDERABLE_TAGS:
        return True
    return False


def get_clone_source(node):
    source_id = node.get(XLINK_HREF)[1:]
    xpath = ".//*[@id='%s']" % (source_id)
    source_node = find_elements(node, xpath)[0]
    return source_node
