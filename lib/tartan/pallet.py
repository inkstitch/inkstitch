# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
# Additional credits to: https://github.com/clsn/pyTartan

import re
from typing import List

import wx
from inkex import Color

from .colors import string_to_color


class Pallet:
    """Holds information about the tartan pallet"""
    def __init__(
        self,
        pallet_code: str = '',
        pallet_stripes: List[list] = [[], []],
        symmetry: bool = True,
        equal_warp_weft: bool = True,
        tt_unit: float = 0.5
    ) -> None:
        """
        :param pallet_code: the pallet code
        :param pallet_stripes: the pallet stripes, lists of warp and weft stripe dictionaries
        :param symmetry: reflective sett (True) / repeating sett (False)
        :param equal_warp_weft:wether warp and weft are equal or not
        :param tt_unit: mm per thread (used for the scottish register threadcount)
        """
        self.pallet_code = pallet_code
        self.pallet_stripes = pallet_stripes
        self.symmetry = symmetry
        self.equal_warp_weft = equal_warp_weft
        self.tt_unit = tt_unit

    def __repr__(self) -> str:
        return self.pallet_code

    def update_symmetry(self, symmetry: bool) -> None:
        self.symmetry = symmetry
        self.update_code()

    def update_from_stripe_sizer(self, sizers: List[wx.BoxSizer], symmetry: bool = True, equal_warp_weft: bool = True) -> None:
        """
        Update pallet code from stripes (customize panel)

        :param sizers: a list of the stripe sizers
        :param symmetry: reflective sett (True) / repeating sett (False)
        :param equal_warp_weft: wether warp and weft are equal or not
        """
        self.symmetry = symmetry
        self.equal_warp_weft = equal_warp_weft

        self.pallet_stripes = [[], []]
        for i, outer_sizer in enumerate(sizers):
            stripes = []
            for stripe_sizer in outer_sizer.Children:
                stripe = {'render': True, 'color': '#000000', 'width': '5'}
                stripe_info = stripe_sizer.GetSizer()
                for color in stripe_info.GetChildren():
                    widget = color.GetWindow()
                    if isinstance(widget, wx.CheckBox):
                        # in embroidery it is ok to have gaps between the stripes
                        if not widget.GetValue():
                            stripe['render'] = False
                    elif isinstance(widget, wx.ColourPickerCtrl):
                        stripe['color'] = widget.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
                    elif isinstance(widget, wx.SpinCtrlDouble):
                        stripe['width'] = widget.GetValue()
                    elif isinstance(widget, wx.Button) or isinstance(widget, wx.StaticText):
                        continue
                stripes.append(stripe)
            self.pallet_stripes[i] = stripes
            if self.equal_warp_weft:
                self.pallet_stripes[1] = stripes
                break
        self.update_code()

    def update_from_code(self, code: str) -> None:
        """
        Update stripes (customize panel) according to the code applied by the user
        Converts code to valid Ink/Stitch code

        :param code: the tartan pattern code to apply
        """
        self.symmetry = True
        if '...' in code:
            self.symmetry = False
        self.equal_warp_weft = True
        if '|' in code:
            self.equal_warp_weft = False
        code = code.replace('/', '')
        code = code.replace('...', '')
        self.pallet_stripes = [[], []]

        if "Threadcount" in code:
            self.parse_threadcount_code(code)
        elif '(' in code:
            self.parse_inkstitch_code(code)
        else:
            self.parse_simple_code(code)

        if self.equal_warp_weft:
            self.pallet_stripes[1] = self.pallet_stripes[0]

        self.update_code()

    def update_code(self) -> None:
        """Updates the pallet code, reading from stripe settings (customize panel)"""
        code = []
        for i, direction in enumerate(self.pallet_stripes):
            for stripe in direction:
                render = '' if stripe['render'] else '?'
                code.append(f"({stripe['color']}){render}{stripe['width']}")
            if i == 0 and self.equal_warp_weft is False:
                code.append("|")
            else:
                break
        if self.symmetry and len(code) > 0:
            code[0] = code[0].replace(')', ')/')
            code[-1] = code[-1].replace(')', ')/')
        code = ' '.join(code)
        if not self.symmetry:
            code = f'...{code}...'
        self.pallet_code = code

    def parse_simple_code(self, code: str) -> None:
        """Example code:
        B24 W4 B24 R2 K24 G24 W2

        Each letter stands for a color defined in .colors.py (if not recognized, defaults to black)
        The number indicates the threadcount (width) of the stripe
        The width of one thread is user defined

        :param code: the tartan pattern code to apply
        """
        stripes = []
        stripe_info = re.findall(r'([a-zA-Z]+)(\?)?([0-9.]*)', code)
        for color, render, width in stripe_info:
            if not width:
                continue
            color = string_to_color(color)
            width = float(width) * self.tt_unit
            if not color:
                color = '#000000'
                render = '?'
            stripes.append({'render': not bool(render), 'color': color, 'width': float(width)})
        self.pallet_stripes[0] = stripes

    def parse_inkstitch_code(self, code: str) -> None:
        """Example code:
        (#0000FF)/2.4 (#FFFFFF)0.4 (#0000FF)2.4 (#FF0000)0.2 (#000000)2.4 (#006400)2.4 (#FFFFFF)/0.2

        |   = separator warp and weft (if not equal)
        /   = indicates a symmetric sett
        ... = indicates an asymmetric sett

        :param code: the tartan pattern code to apply
        """
        code = code.split('|')
        for i, direction in enumerate(code):
            stripes = []
            stripe_info = re.findall(r'\(([0-9A-Za-z#]+)\)(\?)?([0-9.]+)', direction)
            for color, render, width in stripe_info:
                try:
                    # on macOS we need to run wxpython color method inside the app otherwise
                    # the color picker has issues in some cases to accept our input
                    color = wx.Colour(color).GetAsString(wx.C2S_HTML_SYNTAX)
                except wx.PyNoAppError:
                    # however when we render an embroidery element we do not want to open wx.App
                    color = str(Color(color).to_named())
                if not color:
                    color = '#000000'
                    render = False
                stripes.append({'render': not bool(render), 'color': color, 'width': float(width)})
            self.pallet_stripes[i] = stripes

    def parse_threadcount_code(self, code: str) -> None:
        """Read in and work directly from a tartanregister.gov.uk threadcount response
        Example code:
            Threadcount:
            B24W4B24R2K24G24W2

            Pallet:
            B=0000FFBLUE;W=FFFFFFWHITE;R=FF0000RED;K=000000BLACK;G=289C18GREEN;

            Threadcount given over a half sett with full count at the pivots.

        Colors in the threadcount are defined by Letters. The Pallet section declares the rgb value

        :param code: the tartan pattern code to apply
        """
        if 'full sett' in code:
            self.symmetry = False
        else:
            self.symmetry = True

        colors = []
        thread_code = ''
        stripes = []
        lines = code.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if 'Threadcount:' in line and len(lines) > i:
                thread_code = lines[i+1]
            elif line.startswith('Pallet:'):
                pallet = lines[i+1]
                colors = re.findall(r'([A-Za-z]+)=#?([0-9afA-F]{6})', pallet)
                colors = dict(colors)
            i += 1

        stripe_info = re.findall(r'([a-zA-Z]+)([0-9.]*)', thread_code)
        for color, width in stripe_info:
            render = True
            try:
                color = f'#{colors[color]}'
            except KeyError:
                color = '#000000'
                render = False
            width = float(width) * self.tt_unit
            stripes.append({'render': render, 'color': color, 'width': width})

        self.pallet_stripes[0] = stripes

    def get_pallet_width(self, scale: int, min_width: float, direction: int = 0) -> float:
        """
        Get the rendered width of the tartan pallet
        :param scale: the scale value (percent) for the pattern
        :param min_width: min stripe width (before it is rendered as running stitch).
            Smaller stripes have 0 width.
        :param direction: 0 (warp) or 1 (weft)
        :returns: the width of all tartan stripes in given direction
        """
        width = 0
        for stripe in self.pallet_stripes[direction]:
            stripe_width = stripe['width'] * (scale / 100)
            if stripe_width >= min_width or not stripe['render']:
                width += stripe_width
        return width
