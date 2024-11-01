# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from shapely.geometry import MultiPolygon, Polygon
from shapely.validation import make_valid

from ..elements import EmbroideryElement
from ..utils import ensure_multi_polygon
from .tags import SVG_GROUP_TAG


def get_clip_path(node):
    # get clip and apply node transform
    clip = _clip_paths(node)
    for group in node.iterancestors(SVG_GROUP_TAG):
        group_clip = _clip_paths(group)
        if clip and group_clip:
            clip = clip.intersection(group_clip)
        elif group_clip:
            clip = group_clip
    if clip:
        return ensure_multi_polygon(clip)


def _clip_paths(node_or_group):
    clip = node_or_group.clip
    if clip is None:
        return
    transform = node_or_group.composed_transform()
    clip.transform = transform
    clip_element = EmbroideryElement(clip)
    clip_paths = [path for path in clip_element.paths if len(path) > 3]
    if clip_paths:
        clip_paths.sort(key=lambda point_list: Polygon(point_list).area, reverse=True)
        return make_valid(MultiPolygon([(clip_paths[0], clip_paths[1:])]))
