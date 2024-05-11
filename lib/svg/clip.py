# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from shapely.geometry import MultiPolygon, Polygon

from ..elements import EmbroideryElement


def get_clip_path(node):
    # get clip and apply node transform
    clip = node.clip
    transform = node.composed_transform()
    clip.transform = transform
    clip_element = EmbroideryElement(clip)
    clip_paths = [path for path in clip_element.paths if len(path) > 3]
    clip_paths.sort(key=lambda point_list: Polygon(point_list).area, reverse=True)
    if clip_paths:
        return MultiPolygon([(clip_paths[0], clip_paths[1:])])
    return MultiPolygon()
