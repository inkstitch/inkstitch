# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections import defaultdict
from copy import copy
from unicodedata import normalize

from inkex import paths, transforms, units

from ..svg import get_correction_transform, get_guides
from ..svg.tags import (CONNECTION_END, SVG_GROUP_TAG, SVG_PATH_TAG,
                        SVG_USE_TAG, XLINK_HREF)


class Glyph(object):
    """Represents a single character in a single font variant.

    For example, the font inkstitch_small may have variants for left-to-right,
    right-to-left, etc.  Each variant would have a set of Glyphs, one for each
    character in that variant.

    Properties:
      width -- total width of this glyph including all component satins
      node  -- svg:g XML node containing the component satins in this character
    """

    def __init__(self, group):
        """Create a Glyph.

        The nodes will be copied out of their parent SVG document (with nested
        transforms applied).  The original nodes will be unmodified.

        Arguments:
          group -- an svg:g XML node containing all the paths that make up
            this Glyph.  Nested groups are allowed.
        """

        self.name = group.label
        if len(self.name) > 11:
            self.name = normalize('NFC', self.name[11:])
        self._process_baseline(group.getroottree().getroot())
        self.clips = self._process_clips(group)
        self.node = self._process_group(group)
        self._process_bbox()
        self._move_to_origin()
        self._process_commands()

    def _process_clips(self, group):
        clips = defaultdict(list)
        for node in group.iterdescendants():
            if node.clip:
                node_id = node.get_id()
                clips[node_id] = node.clip
        return clips

    def _process_group(self, group):
        new_group = copy(group)
        # new_group.attrib.pop('transform', None)
        # delete references to the original group's children
        del new_group[:]

        for node in group:
            if node.tag == SVG_GROUP_TAG:
                new_group.append(self._process_group(node))
            else:
                node_copy = copy(node)
                transform = -transforms.Transform(get_correction_transform(node, True))

                if "d" in node.attrib:
                    node_copy.path = node.path.transform(transform)

                if not node.tag == SVG_USE_TAG:
                    # Delete transforms from paths and groups, since we applied
                    # them to the paths already.
                    node_copy.attrib.pop('transform', None)
                else:
                    oldx = node.get('x', 0)
                    oldy = node.get('y', 0)
                    x, y = transform.apply_to_point((oldx, oldy))
                    node_copy.set('x', x)
                    node_copy.set('y', y)

                new_group.append(node_copy)

        return new_group

    def _process_baseline(self, svg):
        for guide in get_guides(svg):
            if guide.label == "baseline":
                self.baseline = guide.position.y
                break
        else:
            # no baseline guide found, assume 0 for lack of anything better to use...
            self.baseline = 0

    def _process_bbox(self):
        bbox = [paths.Path(node.get("d")).bounding_box() for node in self.node.iterdescendants(SVG_PATH_TAG) if not node.get(CONNECTION_END, None)]
        left, right = min([box.left for box in bbox]), max([box.right for box in bbox])
        self.width = right - left
        self.min_x = left

    def _process_commands(self):
        # Save object ids with commands in a dictionary: {object_id: [connector_id, symbol_id]}
        self.commands = {}

        for node in self.node.iter(SVG_USE_TAG):
            xlink = node.get(XLINK_HREF, ' ')
            if not xlink.startswith('#inkstitch_'):
                continue

            try:
                connector = self.node.xpath(".//*[@inkscape:connection-start='#%s']" % node.get('id', ' '))[0]
                command_object = connector.get(CONNECTION_END)[1:]
                try:
                    self.commands[command_object].append([connector.get_id(), node.get_id()])
                except KeyError:
                    self.commands[command_object] = [[connector.get_id(), node.get_id()]]
            except (IndexError, TypeError):
                pass

    def _move_to_origin(self):
        translate_x = -self.min_x
        translate_y = -self.baseline
        transform = transforms.Transform("translate(%s, %s)" % (translate_x, translate_y))

        for node in self.node.iter(SVG_PATH_TAG):
            path = paths.Path(node.get("d"))
            path = path.transform(transform)
            node.set('d', str(path))
            node.attrib.pop('transform', None)

        # Move commands as well
        for node in self.node.iter(SVG_USE_TAG):
            oldx = units.convert_unit(node.get("x", 0), 'px', node.unit)
            oldy = units.convert_unit(node.get("y", 0), 'px', node.unit)
            x, y = transform.apply_to_point((oldx, oldy))
            node.set('x', x)
            node.set('y', y)

        # transform clips
        for node in self.node.iterdescendants():
            node_id = node.get_id()
            if node_id in self.clips:
                clip = self.clips[node_id]
                for childnode in clip.iterchildren():
                    childnode.transform @= transform
