# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex
from shapely.geometry import Point

from ..elements import SatinColumn
from ..i18n import _
from ..svg import get_correction_transform
from .base import InkstitchExtension


class CutSatin(InkstitchExtension):
    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selection or not any([isinstance(element, SatinColumn) for element in self.elements]):
            inkex.errormsg(_("Please select one or more satin columns to cut."))
            return

        for satin in self.elements:
            if isinstance(satin, SatinColumn):
                old_satin = satin
                self.split = False
                transform = get_correction_transform(satin.node)
                parent = satin.node.getparent()
                self.index = parent.index(satin.node)
                self.label_index = 0

                commands = satin.get_commands("satin_cut_point")

                if commands is None:
                    # L10N will have the satin's id prepended, like this:
                    # path12345: error: this satin column does not ...
                    satin.fatal(_('this satin column does not have a "satin column cut point" command attached to it. '
                                  'Please use the "Attach commands" extension and attach the "Satin Column cut point" command first.'))

                commands.sort(key=lambda command: satin.center_line.project(Point(command.target_point)), reverse=True)

                satins = [None, None]
                for command in commands:
                    satins = self.split_satin(satin, command)
                    if None in satins:
                        continue
                    self.insert_satin(satins[1], parent, transform)
                    satin = satins[0]
                if satins[0] is not None:
                    self.insert_satin(satins[0], parent, transform)
                if self.split:
                    old_satin.node.delete()

    def insert_satin(self, satin, parent, transform):
        if satin is None:
            return
        node = satin.node
        label = node.label or satin.node.get_id()
        node.set('transform', transform)
        parent.insert(self.index, node)
        node.set('inkscape:label', f'{label} {self.label_index}')
        node.apply_transform()
        self.label_index += 1
        self.split = True

    def split_satin(self, satin, command):
        split_point = command.target_point
        command_group = command.use.getparent()
        if command_group is not None and command_group.get('id').startswith('command_group'):
            command_group.delete()
        else:
            command.use.delete()
            command.connector.delete()

        new_satins = satin.split(split_point)
        return new_satins
