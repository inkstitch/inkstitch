# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import wx

from ..i18n import _
from ..utils.cache import get_stitch_plan_cache
from ..utils.settings import global_settings


class PreferencesFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.extension = kwargs.pop("extension")
        wx.Frame.__init__(self, None, wx.ID_ANY, _("Preferences"), *args, **kwargs)
        self.SetTitle(_("Preferences"))

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        metadata = self.extension.get_inkstitch_metadata()

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(self.panel_1, wx.ID_ANY)
        main_sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 10)

        self.this_svg_page = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.this_svg_page, _("This SVG"))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        # add space above and below to center sizer_2 vertically
        sizer_1.Add((0, 20), 1, wx.EXPAND, 0)

        sizer_2 = wx.FlexGridSizer(2, 4, 15, 10)
        sizer_1.Add(sizer_2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        label_1 = wx.StaticText(self.this_svg_page, wx.ID_ANY, _("Minimum jump stitch length"), style=wx.ALIGN_LEFT)
        label_1.SetToolTip(_("Jump stitches smaller than this will be treated as normal stitches."))
        sizer_2.Add(label_1, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)

        self.minimum_jump_stitch_length = wx.SpinCtrlDouble(
            self.this_svg_page, wx.ID_ANY, inc=0.1,
            value=str(metadata['collapse_len_mm'] or global_settings['default_collapse_len_mm']),
            style=wx.ALIGN_RIGHT | wx.SP_ARROW_KEYS
        )
        self.minimum_jump_stitch_length.SetDigits(1)
        sizer_2.Add(self.minimum_jump_stitch_length, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        label_2 = wx.StaticText(self.this_svg_page, wx.ID_ANY, _("mm"))
        sizer_2.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)

        self.button_1 = wx.Button(self.this_svg_page, wx.ID_ANY, _("Set As Default"))
        sizer_2.Add(self.button_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        label_3 = wx.StaticText(self.this_svg_page, wx.ID_ANY, _("Minimum stitch length"))
        sizer_2.Add(label_3, 0, 0, 0)

        self.minimum_stitch_length = wx.SpinCtrlDouble(
            self.this_svg_page, wx.ID_ANY, inc=0.1,
            value=str(metadata['min_stitch_len_mm'] or global_settings['default_min_stitch_len_mm']),
            style=wx.ALIGN_RIGHT | wx.SP_ARROW_KEYS
        )
        self.minimum_stitch_length.SetDigits(1)
        sizer_2.Add(self.minimum_stitch_length, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        label_4 = wx.StaticText(self.this_svg_page, wx.ID_ANY, _("mm"))
        sizer_2.Add(label_4, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.button_2 = wx.Button(self.this_svg_page, wx.ID_ANY, _("Set As Default"))
        sizer_2.Add(self.button_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_1.Add((0, 20), 1, wx.EXPAND, 0)

        self.global_page = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.global_page, _("Global"))

        sizer_3 = wx.BoxSizer(wx.VERTICAL)

        # add space above and below to center sizer_4 vertically
        sizer_3.Add((0, 20), 1, wx.EXPAND, 0)

        sizer_4 = wx.FlexGridSizer(3, 4, 15, 10)
        sizer_3.Add(sizer_4, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        label_5 = wx.StaticText(self.global_page, wx.ID_ANY, _("Default minimum jump stitch length"), style=wx.ALIGN_LEFT)
        label_5.SetToolTip(_("Jump stitches smaller than this will be treated as normal stitches."))
        sizer_4.Add(label_5, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)

        self.default_minimum_jump_stitch_length = wx.SpinCtrlDouble(
            self.global_page, wx.ID_ANY, inc=0.1,
            value=str(global_settings['default_collapse_len_mm']),
            style=wx.ALIGN_RIGHT | wx.SP_ARROW_KEYS
        )
        self.default_minimum_jump_stitch_length.SetDigits(1)
        sizer_4.Add(self.default_minimum_jump_stitch_length, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        label_6 = wx.StaticText(self.global_page, wx.ID_ANY, _("mm"))
        sizer_4.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)

        sizer_4.Add((0, 0), 0, 0, 0)

        label_7 = wx.StaticText(self.global_page, wx.ID_ANY, _("Minimum stitch length"))
        sizer_4.Add(label_7, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.default_minimum_stitch_length = wx.SpinCtrlDouble(
            self.global_page, wx.ID_ANY, inc=0.1,
            value=str(global_settings['default_min_stitch_len_mm']),
            style=wx.ALIGN_RIGHT | wx.SP_ARROW_KEYS
        )
        self.default_minimum_stitch_length.SetDigits(1)
        sizer_4.Add(self.default_minimum_stitch_length, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        label_8 = wx.StaticText(self.global_page, wx.ID_ANY, _("mm"))
        sizer_4.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_4.Add((0, 20), 0, 0, 0)

        label_9 = wx.StaticText(self.global_page, wx.ID_ANY, _("Stitch plan cache size"), style=wx.ALIGN_LEFT)
        label_9.SetToolTip(_("Jump stitches smaller than this will be treated as normal stitches."))
        sizer_4.Add(label_9, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.stitch_plan_cache_size = wx.SpinCtrl(
            self.global_page, wx.ID_ANY,
            value=str(global_settings['cache_size']),
            style=wx.ALIGN_RIGHT | wx.SP_ARROW_KEYS
        )
        self.stitch_plan_cache_size.SetIncrement(10)
        sizer_4.Add(self.stitch_plan_cache_size, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        label_10 = wx.StaticText(self.global_page, wx.ID_ANY, _("MB"))
        sizer_4.Add(label_10, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.clear_cache_button = wx.Button(self.global_page, wx.ID_ANY, _("Clear Stitch Plan Cache"))
        sizer_4.Add(self.clear_cache_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_3.Add((0, 0), 1, wx.EXPAND, 0)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(button_sizer, 0, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        button_sizer.Add((0, 0), 1, 0, 0)

        self.cancel_button = wx.Button(self.panel_1, wx.ID_CANCEL, "")
        button_sizer.Add(self.cancel_button, 0, wx.RIGHT, 10)

        self.ok_button = wx.Button(self.panel_1, wx.ID_OK, "")
        button_sizer.Add(self.ok_button, 0, 0, 0)

        sizer_4.AddGrowableCol(0)

        self.global_page.SetSizer(sizer_3)

        sizer_2.AddGrowableCol(0)

        self.this_svg_page.SetSizer(sizer_1)

        self.panel_1.SetSizer(main_sizer)

        main_sizer.Fit(self)
        self.Layout()
        self.SetSizeHints(main_sizer.CalcMin())

        self.Bind(wx.EVT_BUTTON, self.set_as_default_minimum_jump_stitch_length, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.set_as_default_minimum_stitch_length, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.clear_cache, self.clear_cache_button)
        self.Bind(wx.EVT_BUTTON, self.cancel_button_clicked, self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.ok_button_clicked, self.ok_button)

    def set_as_default_minimum_jump_stitch_length(self, event):
        self.default_minimum_jump_stitch_length.SetValue(self.minimum_jump_stitch_length.GetValue())

    def set_as_default_minimum_stitch_length(self, event):
        self.default_minimum_stitch_length.SetValue(self.minimum_stitch_length.GetValue())

    def clear_cache(self, event):
        stitch_plan_cache = get_stitch_plan_cache()
        stitch_plan_cache.clear(retry=True)

    def apply(self):
        metadata = self.extension.get_inkstitch_metadata()
        metadata['min_stitch_len_mm'] = self.minimum_stitch_length.GetValue()
        metadata['collapse_len_mm'] = self.minimum_jump_stitch_length.GetValue()

        global_settings['default_min_stitch_len_mm'] = self.default_minimum_stitch_length.GetValue()
        global_settings['default_collapse_len_mm'] = self.default_minimum_jump_stitch_length.GetValue()
        global_settings['cache_size'] = self.stitch_plan_cache_size.GetValue()

        # cache size may have changed
        stitch_plan_cache = get_stitch_plan_cache()
        stitch_plan_cache.size_limit = int(global_settings['cache_size'] * 1024 * 1024)
        stitch_plan_cache.cull()

    def cancel_button_clicked(self, event):
        self.Destroy()

    def ok_button_clicked(self, event):
        self.apply()
        self.Destroy()


class PreferencesApp(wx.App):
    def __init__(self, extension):
        self.extension = extension
        super().__init__()

    def OnInit(self):
        self.frame = PreferencesFrame(extension=self.extension)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = PreferencesApp(None)
    app.MainLoop()
