# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..elements import FillStitch, SatinColumn, Stroke
from ..gui.element_info import ElementInfoApp
from ..i18n import _
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import PIXELS_PER_MM
from .base import InkstitchExtension


class ElementInfo(InkstitchExtension):

    def effect(self):
        if not self.svg.selection or not self.get_elements():
            return

        self.metadata = self.get_inkstitch_metadata()
        self.list_items = []
        self.max_stitch_lengths = []
        self.min_stitch_lengths = []

        previous_stitch_group = None
        for element in self.elements:
            previous_stitch_group = self._element_info(element, previous_stitch_group)
        self._general_info()

        app = ElementInfoApp(self.list_items)
        app.MainLoop()

    def _element_info(self, element, previous_stitch_group):
        stitch_groups = element.to_stitch_groups(previous_stitch_group)
        stitch_plan = stitch_groups_to_stitch_plan(
            stitch_groups,
            collapse_len=self.metadata['collapse_len_mm'],
            min_stitch_len=self.metadata['min_stitch_len_mm']
        )

        self.list_items.append(ListItem(
            name=f"{ element.node.label } ({ element.node.get_id() })",
            value=stitch_groups[0].color,
            headline=True
        ))
        self.list_items.append(ListItem(
            name=_("Type"),
            value=element.element_name
        ))
        if isinstance(element, FillStitch):
            fill_method = next((method.name for method in element._fill_methods if method.id == element.fill_method), "")
            self.list_items.append(ListItem(
                name=_("Fill Method"),
                value=fill_method
            ))

        if isinstance(element, SatinColumn):
            satin_method = next((method.name for method in element._satin_methods if method.id == element.satin_method), "")
            self.list_items.append(ListItem(
                name=_("Satin Method"),
                value=satin_method
            ))

        if isinstance(element, Stroke):
            stroke_method = next((method.name for method in element._stroke_methods if method.id == element.stroke_method), "")
            self.list_items.append(ListItem(
                name=_("Stroke Method"),
                value=stroke_method
            ))

        self.list_items.append(ListItem(
            name=_("Dimensions (mm)"),
            value="{:.2f} x {:.2f}".format(stitch_plan.dimensions_mm[0], stitch_plan.dimensions_mm[1])
        ))

        stitch_lengths = []
        removed_stitches = 0
        for group in stitch_groups:
            stitches = group.stitches

            previous_stitch = stitches[0]
            for stitch in stitches[1:]:
                st = stitch - previous_stitch
                length = st.length() / PIXELS_PER_MM
                if length <= self.metadata['min_stitch_len_mm']:
                    removed_stitches += 1
                    continue
                stitch_lengths.append(length)
                previous_stitch = stitch

        if stitch_lengths:
            self.max_stitch_lengths.append(max(stitch_lengths))
            self.min_stitch_lengths.append(min(stitch_lengths))
        else:
            self.max_stitch_lengths.append(0)
            self.min_stitch_lengths.append(0)
            self.list_items.append(ListItem(
                name=_("Stitches"),
                value="0",
                warning=True
            ))
            self.list_items.append(ListItem(
                name=_("Small stitches (removed)"),
                value=str(removed_stitches)
            ))
            return stitch_groups[0]

        stitches_per_group = ""
        if len(stitch_groups) > 1:
            stitches_per_group = f" ({', '.join([str(len(group.stitches)) for group in stitch_groups]) })"

        self.list_items.append(ListItem(
            name=_("Stitches"),
            value=str(stitch_plan.num_stitches - stitch_plan.num_jumps) + stitches_per_group
        ))
        self.list_items.append(ListItem(
            name=_("Small stitches (removed)"),
            value=str(removed_stitches)
        ))
        self.list_items.append(ListItem(
            name=_("Jumps"),
            value=str(stitch_plan.num_jumps - 1)
        ))
        self.list_items.append(ListItem(
            name=_("Max stitch length"),
            value="{:.2f}".format(max(stitch_lengths))
        ))
        self.list_items.append(ListItem(
            name=_("Min stitch length"),
            value="{:.2f}".format(min(stitch_lengths))
        ))
        self.list_items.append(ListItem())
        return stitch_groups[0]

    def _general_info(self):
        general_info_list_items = []
        stitch_groups = self.elements_to_stitch_groups(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(
            stitch_groups,
            collapse_len=self.metadata['collapse_len_mm'],
            min_stitch_len=self.metadata['min_stitch_len_mm']
        )

        general_info_list_items.append(ListItem(
            name=_("All Selected Elements"),
            headline=True
        ))
        general_info_list_items.append(ListItem(
            name=_("Dimensions (mm)"),
            value="{:.2f} x {:.2f}".format(stitch_plan.dimensions_mm[0], stitch_plan.dimensions_mm[1])
        ))
        general_info_list_items.append(ListItem(
            name=_("Colors"),
            value=str(stitch_plan.num_colors)
        ))
        general_info_list_items.append(ListItem(
            name=_("Color Changes"),
            value=str(stitch_plan.num_color_blocks - 1)
        ))
        general_info_list_items.append(ListItem(
            name=_("Jumps"),
            value=str(stitch_plan.num_jumps - 1)
        ))
        general_info_list_items.append(ListItem(
            name=_("Trims"),
            value=str(stitch_plan.num_trims)
        ))
        general_info_list_items.append(ListItem(
            name=_("Stops"),
            value=str(stitch_plan.num_stops)
        ))
        general_info_list_items.append(ListItem(
            name=_("Stitches"),
            value=str(stitch_plan.num_stitches - stitch_plan.num_jumps)
        ))
        general_info_list_items.append(ListItem(
            name=_("Min stitch length"),
            value="{:.2f}".format(min(self.min_stitch_lengths))
        ))
        general_info_list_items.append(ListItem(
            name=_("Max stitch length"),
            value="{:.2f}".format(max(self.max_stitch_lengths))
        ))
        general_info_list_items.append(ListItem(
            name=_("Filter stitches smaller than (mm)"),
            value=str(self.metadata['min_stitch_len_mm'])
        ))
        general_info_list_items.append(ListItem())

        self.list_items = general_info_list_items + self.list_items


class ListItem:
    def __init__(self, name="", value="", headline=False, warning=False):
        self.name: str = name
        self.value: str = value
        self.headline: bool = headline
        self.warning: bool = warning

    def __repr__(self):
        return f"ListItem({self.name}, {self.value}, {self.headline}, {self.warning})"
