# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from shapely.geometry import MultiPolygon, Polygon
from shapely.validation import make_valid

from ..utils import ensure_multi_polygon
from .tags import SVG_GROUP_TAG, SVG_PATH_TAG


def get_clips(node):
    clips = []
    for element in node.iterancestors(SVG_GROUP_TAG):
        if element.clip is not None:
            clips.append(element.clip)
    return clips


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
    # avoid circular import for EmbroideryElement
    from ..elements import EmbroideryElement

    clip = node_or_group.clip
    if clip is None:
        return
    transform = node_or_group.composed_transform()
    clip.transform = transform
    clip_element = EmbroideryElement(clip)
    path_effect = _get_path_effects(node_or_group)
    clip_paths = None
    if path_effect == 'ignore':
        return
    elif path_effect == 'inverse':
        for path in clip.iterdescendants(SVG_PATH_TAG):
            if path.get('class', None) == 'powerclip':
                original_transform = path.transform
                path.transform @= transform
                clip_element = EmbroideryElement(path)
                clip_paths = [path for path in clip_element.paths if len(path) > 3]
                path.transform = original_transform
                break
    else:
        clip_paths = [path for path in clip_element.paths if len(path) > 3]

    if clip_paths:
        clip_paths.sort(key=lambda point_list: Polygon(point_list).area, reverse=True)
        return make_valid(MultiPolygon([(clip_paths[0], clip_paths[1:])]))


def _get_path_effects(node):
    path_effects = node.get('inkscape:path-effect', None)
    if path_effects is not None:
        path_effects = path_effects.split(';')
        for path_effect in path_effects:
            effect = node.getroottree().getroot().getElementById(path_effect[1:])
            if effect.get('effect', None) == 'powerclip':
                if effect.get('hide_clip', 'false') in ['1', 'true', 'True']:
                    # The clip is inactive
                    return 'ignore'
                elif effect.get('flatten', 'false') in ['1', 'true', 'True']:
                    # Clipping is already calculated into the path.
                    # This means we can ignore the clip.
                    return 'ignore'
                elif effect.get('inverse', 'false') in ['1', 'true', 'True']:
                    return 'inverse'
                else:
                    return 'effect'
    return 'standard'
