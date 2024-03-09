# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import subprocess
import sys

from inkex import Boolean

from ..elements import Clone, FillStitch, Polyline, SatinColumn, Stroke
from ..i18n import _
from ..utils import get_bundled_dir
from .base import InkstitchExtension


class SelectElements(InkstitchExtension):
    def add_arguments(self, pars):
        self.arg_parser.add_argument("--options", type=str, dest="notebook")
        pars.add_argument("--stitch-type", type=str, dest="stitch_type")
        pars.add_argument("--info", type=str, dest="info")

        pars.add_argument("--select-running-stitch", type=Boolean, dest="running", default=False)
        pars.add_argument("--running-stitch-condition", type=str, dest="running_stitch_condition", default="all")
        pars.add_argument("--select-ripples", type=Boolean, dest="ripples", default=False)
        pars.add_argument("--select-zigzag", type=Boolean, dest="zigzag", default=False)
        pars.add_argument("--select-manual", type=Boolean, dest="manual", default=False)
        pars.add_argument("--select-polyline", type=Boolean, dest="poly", default=False)
        pars.add_argument("--select-satin", type=Boolean, dest="satin", default=False)
        pars.add_argument("--satin-underlay", type=str, dest="satin_underlay", default="all")
        pars.add_argument("--rung-count", type=str, dest="rung_count", default="all")
        pars.add_argument("--select-e", type=Boolean, dest="e", default=False)
        pars.add_argument("--select-s", type=Boolean, dest="s", default=False)
        pars.add_argument("--select-satin-zigzag", type=Boolean, dest="satin_zigzag", default=False)
        pars.add_argument("--select-auto-fill", type=Boolean, dest="fill", default=False)
        pars.add_argument("--select-contour-fill", type=Boolean, dest="contour", default=False)
        pars.add_argument("--select-guided-fill", type=Boolean, dest="guided", default=False)
        pars.add_argument("--select-meander-fill", type=Boolean, dest="meander", default=False)
        pars.add_argument("--select-circular-fill", type=Boolean, dest="circular", default=False)
        pars.add_argument("--select-linear-gradient-fill", type=Boolean, dest="linear_gradient", default=False)
        pars.add_argument("--select-legacy-fill", type=Boolean, dest="legacy", default=False)
        pars.add_argument("--fill-underlay", type=str, dest="fill_underlay", default="all")
        pars.add_argument("--select-clone", type=Boolean, dest="clone", default=False)

        pars.add_argument("--python-path", type=str, dest="python_path", default='')

    def effect(self):
        py_path, file_path = self._get_paths()
        id_list = self._get_id_list()

        with subprocess.Popen(
                [py_path, 'select_elements.py', id_list],
                cwd=file_path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL) as proc:
            proc.wait()

    def _get_paths(self):
        file_path = get_bundled_dir("dbus")

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            if sys.platform == "linux":
                py_path = "python3"
            elif sys.platform.startswith("win"):
                # sadly we cannot access python interpreters, so we have to guess the file path in windows
                # and we could be very wrong
                py_path = 'c:/program files/inkscape/bin/python.exe'
            elif sys.platform == "darwin":
                py_path = '/Applications/Inkscape.app/Contents/Resources/bin/python3'
                py_path = 'python3'
        else:
            # we are running a local install
            py_path = sys.executable

        # custom python path
        if self.options.python_path:
            py_path = self.options.python_path

        return py_path, file_path

    def _get_id_list(self):
        if not self.get_elements():
            return ''

        ids = set()
        for element in self.elements:
            if isinstance(element, Stroke) and self._select_stroke(element):
                ids.add(element.id)
            elif isinstance(element, Polyline) and self.options.poly:
                ids.add(element.id)
            elif isinstance(element, FillStitch) and self._select_fill(element):
                ids.add(element.id)
            elif isinstance(element, SatinColumn) and self._select_satin(element):
                ids.add(element.id)
            elif isinstance(element, Clone) and self.options.clone:
                ids.add(element.id)

        return ','.join(ids)

    def _select_stroke(self, element):
        select = False
        method = element.stroke_method
        if self.options.running and method == 'running_stitch' and self._running_condition(element):
            select = True
        if self.options.ripples and method == 'ripple_stitch':
            select = True
        elif self.options.zigzag and method == 'zigzag_stitch':
            select = True
        elif self.options.manual and method == 'manual_stitch':
            select = True
        return select

    def _select_fill(self, element):
        select = False
        if not self._select_fill_underlay(element):
            return False
        method = element.fill_method
        if self.options.fill and method == 'auto_fill':
            select = True
        elif self.options.contour and method == 'contour_fill':
            select = True
        elif self.options.guided and method == 'guided_fill':
            select = True
        elif self.options.meander and method == 'meander_fill':
            select = True
        elif self.options.circular and method == 'circular_fill':
            select = True
        elif self.options.linear_gradient and method == 'linear_gradient_fill':
            select = True
        elif self.options.legacy and method == 'legacy_fill':
            select = True
        return select

    def _running_condition(self, element):
        element_id = element.node.get_id() or ''
        conditions = {'all': True, 'autorun-top': element_id.startswith('autorun'), 'autorun-underpath': element_id.startswith('underpath')}
        return conditions[self.options.running_stitch_condition]

    def _select_fill_underlay(self, element):
        underlay = {'all': True, 'no': not element.fill_underlay, 'yes': element.fill_underlay}
        return underlay[self.options.fill_underlay]

    def _select_satin(self, element):
        select = False
        if not self._select_satin_underlay(element):
            return False
        if not self._select_rung_count(element):
            return False
        method = element.satin_method
        if self.options.satin and method == "satin_column":
            select = True
        elif self.options.e and method == "e_stitch":
            select = True
        elif self.options.s and method == "s_stitch":
            select = True
        elif self.options.satin_zigzag and method == "zigzag":
            select = True
        return select

    def _select_satin_underlay(self, element):
        underlay = {'all': None, 'no': None, 'center': None, 'contour': None, 'zigzag': None}
        underlay['center'] = element.center_walk_underlay
        underlay['contour'] = element.contour_underlay
        underlay['zigzag'] = element.zigzag_underlay
        underlay['no'] = not any(underlay.values())
        underlay['all'] = True
        return underlay[self.options.satin_underlay]

    def _select_rung_count(self, element):
        rung_count = {'all': None, 'zero': None, 'two': None}
        rung_count['zero'] = len(element.paths) == 2
        rung_count['two'] = len(element.paths) == 4
        rung_count['all'] = True
        return rung_count[self.options.rung_count]


if __name__ == '__main__':
    SelectElements().run()
