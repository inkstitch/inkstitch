# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import atan2, degrees, radians

from inkex import CubicSuperPath, Path, Transform
from shapely import MultiLineString

from ..commands import is_command_symbol
from ..i18n import _
from ..svg.path import get_node_transform
from ..svg.tags import (EMBROIDERABLE_TAGS, INKSTITCH_ATTRIBS, SVG_USE_TAG,
                        XLINK_HREF, SVG_GROUP_TAG)
from ..utils import cache
from .element import EmbroideryElement, param
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
        return self.get_float_param('angle') or None

    @property
    @param('flip_angle',
           _('Flip angle'),
           tooltip=_("Flip automatically calucalted angle if it appears to be wrong."),
           type='boolean')
    @cache
    def flip_angle(self):
        return self.get_boolean_param('flip_angle')

    def get_cache_key_data(self, previous_stitch):
        source_node = get_clone_source(self.node)
        source_elements = self.clone_to_element(source_node)
        return [element.get_cache_key(previous_stitch) for element in source_elements]

    def clone_to_element(self, node):
        from .utils import node_to_elements
        return node_to_elements(node, True)

    def to_stitch_groups(self, last_patch=None):
        patches = []

        source_node = get_clone_source(self.node)
        if source_node.tag not in EMBROIDERABLE_TAGS and source_node.tag != SVG_GROUP_TAG:
            return []

        old_transform = source_node.get('transform', '')
        source_transform = source_node.composed_transform()
        source_path = Path(source_node.get_path()).transform(source_transform)
        transform = Transform(source_node.get('transform', '')) @ -source_transform
        transform @= self.node.composed_transform() @ Transform(source_node.get('transform', ''))
        source_node.set('transform', transform)

        old_angle = float(source_node.get(INKSTITCH_ATTRIBS['angle'], 0))
        if self.clone_fill_angle is None:
            rot = transform.add_rotate(-old_angle)
            angle = self._get_rotation(rot, source_node, source_path)
            if angle is not None:
                source_node.set(INKSTITCH_ATTRIBS['angle'], angle)
        else:
            source_node.set(INKSTITCH_ATTRIBS['angle'], self.clone_fill_angle)

        elements = self.clone_to_element(source_node)
        for element in elements:
            stitch_groups = element.to_stitch_groups(last_patch)
            patches.extend(stitch_groups)

        source_node.set('transform', old_transform)
        source_node.set(INKSTITCH_ATTRIBS['angle'], old_angle)
        return patches

    def _get_rotation(self, transform, source_node, source_path):
        try:
            rotation = transform.rotation_degrees()
        except ValueError:
            source_path = CubicSuperPath(source_path)[0]
            clone_path = Path(source_node.get_path()).transform(source_node.composed_transform())
            clone_path = CubicSuperPath(clone_path)[0]

            angle_source = atan2(source_path[1][1][1] - source_path[0][1][1], source_path[1][1][0] - source_path[0][1][0])
            angle_clone = atan2(clone_path[1][1][1] - clone_path[0][1][1], clone_path[1][1][0] - clone_path[0][1][0])
            angle_embroidery = radians(-float(source_node.get(INKSTITCH_ATTRIBS['angle'], 0)))

            diff = angle_source - angle_embroidery
            rotation = degrees(diff + angle_clone)

            if self.flip_angle:
                rotation = -degrees(diff - angle_clone)

        return -rotation

    def get_clone_style(self, style_name, node, default=None):
        style = node.style[style_name] or default
        return style

    def center(self, source_node):
        transform = get_node_transform(self.node.getparent())
        center = self.node.bounding_box(transform).center
        return center

    @property
    def shape(self):
        path = self.node.get_path()
        transform = Transform(self.node.composed_transform())
        path = path.transform(transform)
        path = path.to_superpath()
        return MultiLineString(path)

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
    return node.href
