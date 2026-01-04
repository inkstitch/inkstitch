# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import os

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from ...debug.debug import debug
from ...i18n import _
from . import SimulatorPreferenceDialog
from . import DesignInfoDialog
from .export_video_dialog import ExportVideoDialog
from .export_image_dialog import ExportImageDialog
from ...utils.settings import global_settings


class ViewPanel(ScrolledPanel):
    """"""

    @debug.time
    def __init__(self, parent, detach_callback):
        """"""
        self.parent = parent
        self.detach_callback = detach_callback
        ScrolledPanel.__init__(self, parent)
        self.SetupScrolling(scroll_y=True, scroll_x=False)

        self.button_style = wx.BU_EXACTFIT | wx.BU_NOTEXT

        self.control_panel = parent.cp

        self.npp_button_status = global_settings["npp_button_status"]
        self.jump_button_status = global_settings["jump_button_status"]
        self.trim_button_status = global_settings["trim_button_status"]
        self.stop_button_status = global_settings["stop_button_status"]
        self.color_change_button_status = global_settings["color_change_button_status"]
        self.toggle_page_button_status = global_settings["toggle_page_button_status"]
        self.display_crosshair_status = global_settings["display_crosshair"]

        self.btnNpp = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnNpp.SetBitmap(self.control_panel.load_icon("npp"))
        self.btnNpp.SetToolTip(_("Display needle penetration point (O)"))
        self.btnNpp.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_npp)
        self.btnNpp.SetValue(self.npp_button_status)
        self.btnJump = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnJump.SetToolTip(_("Show jump stitches"))
        self.btnJump.SetBitmap(self.control_panel.load_icon("jump"))
        self.btnJump.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button("jump", event))
        self.btnJump.SetValue(self.jump_button_status)
        if self.jump_button_status:
            self.control_panel.slider.enable_marker_list("jump")
        self.btnTrim = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnTrim.SetToolTip(_("Show trims"))
        self.btnTrim.SetBitmap(self.control_panel.load_icon("trim"))
        self.btnTrim.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button("trim", event))
        self.btnTrim.SetValue(self.trim_button_status)
        if self.trim_button_status:
            self.control_panel.slider.enable_marker_list("trim")
        self.btnStop = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnStop.SetToolTip(_("Show stops"))
        self.btnStop.SetBitmap(self.control_panel.load_icon("stop"))
        self.btnStop.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button("stop", event))
        self.btnStop.SetValue(self.stop_button_status)
        if self.stop_button_status:
            self.control_panel.slider.enable_marker_list("stop")
        self.btnColorChange = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnColorChange.SetToolTip(_("Show color changes"))
        self.btnColorChange.SetBitmap(self.control_panel.load_icon("color_change"))
        self.btnColorChange.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button("color_change", event))
        self.btnColorChange.SetValue(self.color_change_button_status)
        if self.color_change_button_status:
            self.control_panel.slider.enable_marker_list("color_change")

        self.btnInfo = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnInfo.SetToolTip(_("Open info dialog"))
        self.btnInfo.SetBitmap(self.control_panel.load_icon("info"))
        self.btnInfo.Bind(wx.EVT_TOGGLEBUTTON, self.on_info_button)

        self.btnBackgroundColor = wx.ColourPickerCtrl(self, -1, colour="white", size=((40, -1)))
        self.btnBackgroundColor.SetToolTip(_("Change background color"))
        self.btnBackgroundColor.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_update_background_color)

        self.btnCursor = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnCursor.SetToolTip(_("Show crosshair"))
        self.btnCursor.SetBitmap(self.control_panel.load_icon("cursor"))
        self.btnCursor.SetValue(self.display_crosshair_status)
        self.btnCursor.Bind(wx.EVT_TOGGLEBUTTON, self.on_cursor_button)

        if not self.detach_callback:
            self.btnPage = wx.BitmapToggleButton(self, -1, style=self.button_style)
            self.btnPage.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_page)
            self.btnPage.SetValue(self.toggle_page_button_status)
            self.btnPage.SetBitmap(self.control_panel.load_icon("page"))
            self.btnPage.SetToolTip(_("Show page"))

        self.btnSettings = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnSettings.SetToolTip(_("Open settings dialog"))
        self.btnSettings.SetBitmap(self.control_panel.load_icon("settings"))
        self.btnSettings.Bind(wx.EVT_TOGGLEBUTTON, self.on_settings_button)

        # Export video button with SVG icon
        self.btnExportVideo = wx.BitmapButton(self, -1, style=self.button_style)
        self.btnExportVideo.SetToolTip(_("Export simulation as video file"))
        self.btnExportVideo.SetBitmap(self._load_svg_icon("video"))
        self.btnExportVideo.Bind(wx.EVT_BUTTON, self.on_export_video)

        # Export image button with SVG icon
        self.btnExportImage = wx.BitmapButton(self, -1, style=self.button_style)
        self.btnExportImage.SetToolTip(_("Export simulation as image file"))
        self.btnExportImage.SetBitmap(self._load_svg_icon("image"))
        self.btnExportImage.Bind(wx.EVT_BUTTON, self.on_export_image)

        if self.detach_callback:
            self.btnDetachSimulator = wx.BitmapButton(self, -1, style=self.button_style)
            self.btnDetachSimulator.SetToolTip(_("Detach/attach simulator window"))
            self.btnDetachSimulator.SetBitmap(self.control_panel.load_icon("detach_window"))
            self.btnDetachSimulator.Bind(wx.EVT_BUTTON, lambda event: self.control_panel.detach_callback())

        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        show_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Show")), wx.VERTICAL)
        show_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        show_inner_sizer.Add(self.btnNpp, 0, wx.ALL, 2)
        show_inner_sizer.Add(self.btnJump, 0, wx.ALL, 2)
        show_inner_sizer.Add(self.btnTrim, 0, wx.ALL, 2)
        show_inner_sizer.Add(self.btnStop, 0, wx.ALL, 2)
        show_inner_sizer.Add(self.btnColorChange, 0, wx.ALL, 2)
        show_sizer.Add(0, 2, 0)
        show_sizer.Add(show_inner_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        show_sizer.Add(0, 2, 0)
        outer_sizer.Add(show_sizer, 0, wx.EXPAND)
        outer_sizer.Add(0, 10, 0)

        info_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Info")), wx.VERTICAL)
        info_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        info_inner_sizer.Add(self.btnInfo, 0, wx.EXPAND | wx.ALL, 2)
        info_sizer.Add(0, 2, 0)
        info_sizer.Add(info_inner_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        info_sizer.Add(0, 2, 0)
        outer_sizer.Add(info_sizer, 0, wx.EXPAND)
        outer_sizer.Add(0, 10, 0)

        settings_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Settings")), wx.VERTICAL)
        settings_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        settings_inner_sizer.Add(self.btnBackgroundColor, 0, wx.EXPAND | wx.ALL, 2)
        settings_inner_sizer.Add(self.btnCursor, 0, wx.EXPAND | wx.ALL, 2)
        if not self.detach_callback:
            settings_inner_sizer.Add(self.btnPage, 0, wx.EXPAND | wx.ALL, 2)
        settings_inner_sizer.Add(self.btnSettings, 0, wx.EXPAND | wx.ALL, 2)
        if self.detach_callback:
            settings_inner_sizer.Add(self.btnDetachSimulator, 0, wx.ALL, 2)
        settings_sizer.Add(0, 2, 0)
        settings_sizer.Add(settings_inner_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        settings_sizer.Add(0, 2, 0)
        outer_sizer.Add(settings_sizer, 0, wx.EXPAND)
        outer_sizer.Add(0, 10, 0)

        # Export section
        export_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Export")), wx.VERTICAL)
        export_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        export_inner_sizer.Add(self.btnExportVideo, 0, wx.EXPAND | wx.ALL, 2)
        export_inner_sizer.Add(self.btnExportImage, 0, wx.EXPAND | wx.ALL, 2)
        export_sizer.Add(0, 2, 0)
        export_sizer.Add(export_inner_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        export_sizer.Add(0, 2, 0)
        outer_sizer.Add(export_sizer, 0, wx.EXPAND)

        self.SetSizerAndFit(outer_sizer)

    def set_drawing_panel(self, drawing_panel):
        self.drawing_panel = drawing_panel

    def _load_svg_icon(self, icon_name):
        """Load an SVG icon and convert it to a bitmap.

        Args:
            icon_name: Name of the icon file without extension

        Returns:
            wx.Bitmap of the icon
        """
        try:
            from wx.svg import SVGimage

            icon_path = os.path.join(self.control_panel.icons_dir, f"{icon_name}.svg")
            if os.path.exists(icon_path):
                svg = SVGimage.CreateFromFile(icon_path)
                # Render at button size
                size = self.control_panel.button_size
                bitmap = svg.ConvertToScaledBitmap(wx.Size(size, size))
                return bitmap
        except (ImportError, Exception):
            pass
        # Fallback: return empty bitmap (button will show nothing or default)
        return wx.Bitmap(self.control_panel.button_size, self.control_panel.button_size)

    def on_update_background_color(self, event):
        color = event.Colour
        self.set_background_color(color)
        self.drawing_panel.set_background_color(color)
        self.drawing_panel.Refresh()

    def set_background_color(self, color):
        self.btnBackgroundColor.SetColour(color)

    def on_toggle_npp_shortcut(self, event):
        self.btnNpp.SetValue(not self.btnNpp.GetValue())
        self.toggle_npp(event)

    def toggle_npp(self, event):
        self.drawing_panel.Refresh()
        global_settings["npp_button_status"] = self.btnNpp.GetValue()

    def on_cursor_button(self, event):
        self.drawing_panel.Refresh()
        global_settings["display_crosshair"] = self.btnCursor.GetValue()

    def toggle_page(self, event):
        debug.log("toggle page")
        value = self.btnPage.GetValue()
        self.drawing_panel.set_show_page(value)
        self.drawing_panel.Refresh()
        global_settings["toggle_page_button_status"] = value

    def on_marker_button(self, marker_type, event):
        value = event.GetEventObject().GetValue()
        self.control_panel.slider.enable_marker_list(marker_type, value)
        if marker_type == "jump":
            self.drawing_panel.Refresh()
        global_settings[f"{marker_type}_button_status"] = value

    def on_settings_button(self, event):
        if event.GetEventObject().GetValue():
            self.settings_panel = SimulatorPreferenceDialog(self, title=_("Simulator Preferences"))
            self.settings_panel.Bind(wx.EVT_CLOSE, self.settings_panel_closed)
            self.settings_panel.Show()
        else:
            self.settings_panel.Close()

    def on_info_button(self, event):
        if event.GetEventObject().GetValue():
            self.info_panel = DesignInfoDialog(self, title=_("Design Info"))
            self.info_panel.Bind(wx.EVT_CLOSE, self.info_panel_closed)
            self.info_panel.Show()
        else:
            self.info_panel.Close()

    def info_panel_closed(self, event):
        self.info_panel.Destroy()
        self.info_panel = None
        self.btnInfo.SetValue(False)

    def settings_panel_closed(self, event):
        self.settings_panel.Destroy()
        self.settings_panel = None
        self.btnSettings.SetValue(False)

    def on_export_video(self, event):
        """Open the export video dialog."""
        # Pause animation during export
        self.drawing_panel.stop()

        # Get current background color
        background_color = self.btnBackgroundColor.GetColour()

        # Get stitch count from control panel
        num_stitches = self.control_panel.num_stitches

        # Open export dialog
        dialog = ExportVideoDialog(
            self.GetTopLevelParent(), drawing_panel=self.drawing_panel, num_stitches=num_stitches, background_color=background_color
        )
        dialog.ShowModal()
        dialog.Destroy()

    def on_export_image(self, event):
        """Open the export image dialog."""
        # Pause animation during export
        self.drawing_panel.stop()

        # Get current background color
        background_color = self.btnBackgroundColor.GetColour()

        # Get stitch info from control panel
        num_stitches = self.control_panel.num_stitches
        current_stitch = self.control_panel.current_stitch

        # Open export dialog
        dialog = ExportImageDialog(
            self.GetTopLevelParent(),
            drawing_panel=self.drawing_panel,
            num_stitches=num_stitches,
            current_stitch=current_stitch,
            background_color=background_color,
        )
        dialog.ShowModal()
        dialog.Destroy()
