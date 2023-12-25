# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import re

import wx
from inkex import Color

from .colors import string_to_color


class Pallet:
    def __init__(self, pallet_code='', pallet_stripes=[[], []], symmetry=True, equal_warp_weft=True, tt_unit=0.5):
        self.pallet_code = pallet_code
        self.pallet_stripes = pallet_stripes
        self.symmetry = symmetry
        self.equal_warp_weft = equal_warp_weft
        self.tt_unit = tt_unit

    def __repr__(self):
        return f'Pallet({self.symmetry}, {self.pallet_code}, {self.pallet_stripes})'

    def update_symmetry(self, symmetry):
        self.symmetry = symmetry
        self.update_code()

    def update_from_stripe_sizer(self, sizers, symmetry=True, equal_warp_weft=True):
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

    def update_from_code(self, code):
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

    def update_code(self):
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

    def parse_simple_code(self, code):
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

    def parse_inkstitch_code(self, code):
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

    def parse_threadcount_code(self, code):
        ''' Read in and work directly from a tartanregister.gov.uk threadcount response '''
        if 'full sett' in code:
            self.symmetry = False
        else:
            self.symmetry = True

        self.equal_warp_weft = True

        colors = []
        thread_code = ''
        stripes = []
        lines = code.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if 'Threadcount:' in line and len(lines) > i + 1:
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

    def get_pallet_width(self, scale, min_width, direction=0):
        width = 0
        for stripe in self.pallet_stripes[direction]:
            stripe_width = stripe['width'] * (scale / 100)
            if stripe_width >= min_width or not stripe['render']:
                width += stripe_width
        return width
