# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..elements import FillStitch, SatinColumn, Stroke
from ..gui.abort_message import AbortMessageApp
from ..gui.element_info import ElementInfoApp
from ..i18n import _
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import PIXELS_PER_MM
from .base import InkstitchExtension


class ElementInfo(InkstitchExtension):

    def effect(self):
        if not self.svg.selection or not self.get_elements():
            app = AbortMessageApp(
                _("Please select at least one element."),
                _("https://inkstitch.org/docs/troubleshoot/#element-info")
            )
            app.MainLoop()
            return

        self.metadata = self.get_inkstitch_metadata()
        self.list_items = []
        self.max_stitch_lengths = []
        self.min_stitch_lengths = []
        self.export_txt = "element_id\ttype\tmethod\tdimensions\tstitches\tjumps\tmax_stitch_length\tmin_stitch_length\n"

        next_elements = [None]
        if len(self.elements) > 1:
            next_elements = self.elements[1:] + next_elements
        previous_stitch_group = None
        for element, next_element in zip(self.elements, next_elements):
            text_export, previous_stitch_group = self._element_info(element, previous_stitch_group, next_element)
            self.export_txt += text_export
        self._general_info()
        app = ElementInfoApp(self.list_items, self.export_txt)
        app.MainLoop()

    def _element_info(self, element, previous_stitch_group, next_element):
        stitch_groups = element.embroider(previous_stitch_group, next_element)
        stitch_plan = stitch_groups_to_stitch_plan(
            stitch_groups,
            collapse_len=self.metadata['collapse_len_mm'],
            min_stitch_len=self.metadata['min_stitch_len_mm']
        )
        label = element.node.label
        element_id = element.node.get_id()

        self.list_items.append(ListItem(
            name=f"{label} ({element_id})",
            value=stitch_groups[0].color,
            headline=True
        ))
        element_name = element.element_name
        self.list_items.append(ListItem(
            name=_("Type"),
            value=element_name
        ))
        if isinstance(element, FillStitch):
            fill_method = next((method.name for method in element._fill_methods if method.id == element.fill_method), "")
            method = fill_method
            self.list_items.append(ListItem(
                name=_("Fill Method"),
                value=fill_method
            ))

        if isinstance(element, SatinColumn):
            satin_method = next((method.name for method in element._satin_methods if method.id == element.satin_method), "")
            method = satin_method
            self.list_items.append(ListItem(
                name=_("Satin Method"),
                value=satin_method
            ))

        if isinstance(element, Stroke):
            stroke_method = next((method.name for method in element._stroke_methods if method.id == element.stroke_method), "")
            method = stroke_method
            self.list_items.append(ListItem(
                name=_("Stroke Method"),
                value=stroke_method
            ))
        dimensions = "{:.2f} x {:.2f}".format(stitch_plan.dimensions_mm[0], stitch_plan.dimensions_mm[1])
        self.list_items.append(ListItem(
            name=_("Dimensions (mm)"),
            value=dimensions
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
            return ("", stitch_groups[0])

        stitches_per_group = ""
        if len(stitch_groups) > 1:
            stitches_per_group = f" ({', '.join([str(len(group.stitches)) for group in stitch_groups])})"

        nb_stitches = str(stitch_plan.num_stitches - stitch_plan.num_jumps) + stitches_per_group
        self.list_items.append(ListItem(
            name=_("Stitches"),
            value=nb_stitches
        ))
        self.list_items.append(ListItem(
            name=_("Small stitches (removed)"),
            value=str(removed_stitches)
        ))
        nb_jumps = str(stitch_plan.num_jumps - 1)
        self.list_items.append(ListItem(
            name=_("Jumps"),
            value=nb_jumps
        ))
        max_stitch_length = "{:.2f}".format(max(stitch_lengths))
        self.list_items.append(ListItem(
            name=_("Max stitch length"),
            value=max_stitch_length
        ))
        min_stitch_length = "{:.2f}".format(min(stitch_lengths))
        self.list_items.append(ListItem(
            name=_("Min stitch length"),
            value=min_stitch_length
        ))
        self.list_items.append(ListItem())

        text_export = f"{element_id}\t{element_name}\t{method}\t{dimensions}\t{nb_stitches}\t{nb_jumps}\t{max_stitch_length}\t{min_stitch_length}\n"
        return (text_export, stitch_groups[0])

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
    def __init__(self, name="", value="", headline=False, warning=False) -> None:
        self.name: str = name
        self.value: str = value
        self.headline: bool = headline
        self.warning: bool = warning

    def __repr__(self):
        return f"ListItem({self.name}, {self.value}, {self.headline}, {self.warning})"
