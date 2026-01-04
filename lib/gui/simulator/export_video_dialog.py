# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import threading
import time

import wx

from ...i18n import _
from ...utils.settings import global_settings


class ExportVideoDialog(wx.Dialog):
    """Dialog for exporting embroidery simulation as video."""

    def __init__(self, parent, drawing_panel, num_stitches, background_color, document_name="", **kwargs):
        """Initialize the export video dialog.

        Args:
            parent: Parent window
            drawing_panel: The DrawingPanel instance for frame capture
            num_stitches: Total number of stitches in the design
            background_color: Current background color from simulator
            document_name: Optional name of the document for default filename
        """
        super().__init__(parent, title=_("Export Simulation Video"), **kwargs)

        self.drawing_panel = drawing_panel
        self.num_stitches = num_stitches
        self.background_color = background_color
        self.document_name = document_name
        self.exporting = False
        self.export_thread = None

        self._create_ui()
        self._bind_events()
        self._update_duration()

        self.SetMinSize((450, 400))
        self.Fit()
        self.Centre()

    def _create_ui(self):
        """Create the dialog UI elements."""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Info section
        info_box = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Design Info")), wx.VERTICAL)
        stitch_label = wx.StaticText(self, label=_("Total Stitches: %d") % self.num_stitches)
        info_box.Add(stitch_label, 0, wx.ALL, 5)

        # Stitch range selection (from/to)
        range_sizer = wx.BoxSizer(wx.HORIZONTAL)
        range_sizer.Add(wx.StaticText(self, label=_("From Stitch:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.from_stitch_spin = wx.SpinCtrl(self, value="1", min=1, max=self.num_stitches, initial=1)
        range_sizer.Add(self.from_stitch_spin, 1, wx.EXPAND | wx.RIGHT, 10)
        range_sizer.Add(wx.StaticText(self, label=_("To Stitch:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.to_stitch_spin = wx.SpinCtrl(self, value=str(self.num_stitches), min=1, max=self.num_stitches, initial=self.num_stitches)
        range_sizer.Add(self.to_stitch_spin, 1, wx.EXPAND)
        info_box.Add(range_sizer, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(info_box, 0, wx.EXPAND | wx.ALL, 10)

        # Speed settings
        speed_box = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Export Settings")), wx.VERTICAL)

        # Speed input
        speed_sizer = wx.BoxSizer(wx.HORIZONTAL)
        speed_label = wx.StaticText(self, label=_("Speed (stitches/sec):"))
        self.speed_spin = wx.SpinCtrl(
            self, value=str(global_settings.get("simulator_speed", 100)), min=1, max=10000, initial=global_settings.get("simulator_speed", 100)
        )
        speed_sizer.Add(speed_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        speed_sizer.Add(self.speed_spin, 1, wx.EXPAND)
        speed_box.Add(speed_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Duration display
        duration_sizer = wx.BoxSizer(wx.HORIZONTAL)
        duration_label = wx.StaticText(self, label=_("Video Duration:"))
        self.duration_text = wx.StaticText(self, label="0:00")
        self.duration_text.SetFont(wx.Font(wx.FontInfo(12).Bold()))
        duration_sizer.Add(duration_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        duration_sizer.Add(self.duration_text, 0, wx.ALIGN_CENTER_VERTICAL)
        speed_box.Add(duration_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # FPS input
        fps_sizer = wx.BoxSizer(wx.HORIZONTAL)
        fps_label = wx.StaticText(self, label=_("Frame Rate (FPS):"))
        self.fps_spin = wx.SpinCtrl(self, value="30", min=10, max=60, initial=30)
        fps_sizer.Add(fps_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        fps_sizer.Add(self.fps_spin, 1, wx.EXPAND)
        speed_box.Add(fps_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Format selection (GIF - reliable, widely supported, no external dependencies)
        format_sizer = wx.BoxSizer(wx.HORIZONTAL)
        format_label = wx.StaticText(self, label=_("Format:"))
        self.format_choice = wx.Choice(self, choices=["GIF"])
        self.format_choice.SetSelection(0)
        format_sizer.Add(format_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        format_sizer.Add(self.format_choice, 1, wx.EXPAND)
        speed_box.Add(format_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Resolution selection
        resolution_sizer = wx.BoxSizer(wx.HORIZONTAL)
        resolution_label = wx.StaticText(self, label=_("Resolution:"))
        self.resolution_choice = wx.Choice(
            self, choices=[_("Current Size"), _("Fit Design"), "720p (1280x720)", "1080p (1920x1080)", "4K (3840x2160)", _("Custom")]
        )
        self.resolution_choice.SetSelection(0)
        resolution_sizer.Add(resolution_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        resolution_sizer.Add(self.resolution_choice, 1, wx.EXPAND)
        speed_box.Add(resolution_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Scale multiplier for Fit Design (1x to 10x)
        scale_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scale_label = wx.StaticText(self, label=_("Scale Multiplier:"))
        self.scale_choice = wx.Choice(self, choices=["1x", "2x", "3x", "4x", "5x", "6x", "8x", "10x"])
        self.scale_choice.SetSelection(0)  # Default 1x
        scale_sizer.Add(self.scale_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        scale_sizer.Add(self.scale_choice, 1, wx.EXPAND)
        speed_box.Add(scale_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Custom resolution inputs
        custom_res_sizer = wx.BoxSizer(wx.HORIZONTAL)
        custom_res_sizer.Add(wx.StaticText(self, label=_("Width:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.width_spin = wx.SpinCtrl(self, value="1920", min=100, max=7680, initial=1920)
        custom_res_sizer.Add(self.width_spin, 1, wx.EXPAND | wx.RIGHT, 10)
        custom_res_sizer.Add(wx.StaticText(self, label=_("Height:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.height_spin = wx.SpinCtrl(self, value="1080", min=100, max=4320, initial=1080)
        custom_res_sizer.Add(self.height_spin, 1, wx.EXPAND)
        speed_box.Add(custom_res_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Padding input
        padding_sizer = wx.BoxSizer(wx.HORIZONTAL)
        padding_sizer.Add(wx.StaticText(self, label=_("Padding (px):")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        self.padding_spin = wx.SpinCtrl(self, value="20", min=0, max=200, initial=20)
        padding_sizer.Add(self.padding_spin, 1, wx.EXPAND)
        speed_box.Add(padding_sizer, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(speed_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Display Options
        display_box = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Display Options")), wx.VERTICAL)

        # Crosshair checkbox
        self.crosshair_check = wx.CheckBox(self, label=_("Show Crosshair"))
        self.crosshair_check.SetValue(False)
        display_box.Add(self.crosshair_check, 0, wx.ALL, 5)

        # Needle penetration points checkbox
        self.needle_points_check = wx.CheckBox(self, label=_("Show Needle Penetration Points"))
        self.needle_points_check.SetValue(False)
        display_box.Add(self.needle_points_check, 0, wx.ALL, 5)

        main_sizer.Add(display_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Progress bar (hidden initially)
        self.progress_bar = wx.Gauge(self, range=100, style=wx.GA_HORIZONTAL)
        self.progress_bar.Hide()
        main_sizer.Add(self.progress_bar, 0, wx.EXPAND | wx.ALL, 10)

        # Status text
        self.status_text = wx.StaticText(self, label="")
        main_sizer.Add(self.status_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.export_btn = wx.Button(self, label=_("Export"))
        self.cancel_btn = wx.Button(self, wx.ID_CANCEL, label=_("Cancel"))
        button_sizer.Add(self.export_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.cancel_btn, 0, wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(main_sizer)

    def _bind_events(self):
        """Bind event handlers."""
        self.speed_spin.Bind(wx.EVT_SPINCTRL, self._on_speed_change)
        self.from_stitch_spin.Bind(wx.EVT_SPINCTRL, self._on_range_change)
        self.to_stitch_spin.Bind(wx.EVT_SPINCTRL, self._on_range_change)
        self.resolution_choice.Bind(wx.EVT_CHOICE, self._on_resolution_change)
        self.width_spin.Bind(wx.EVT_SPINCTRL, self._on_width_change)
        self.height_spin.Bind(wx.EVT_SPINCTRL, self._on_height_change)
        self.export_btn.Bind(wx.EVT_BUTTON, self._on_export)
        self.Bind(wx.EVT_CLOSE, self._on_close)

        # Track if we're updating to prevent recursive calls
        self._updating_size = False

        self._update_custom_resolution_state()

    def _get_aspect_ratio(self):
        """Get the design's aspect ratio (width / height)."""
        if self.drawing_panel.height > 0:
            return self.drawing_panel.width / self.drawing_panel.height
        return 16 / 9  # Default fallback

    def _on_width_change(self, event):
        """Handle width change - update height to preserve aspect ratio."""
        if self._updating_size:
            return
        self._updating_size = True
        try:
            aspect_ratio = self._get_aspect_ratio()
            new_width = self.width_spin.GetValue()
            new_height = int(new_width / aspect_ratio)
            self.height_spin.SetValue(max(100, min(4320, new_height)))
        finally:
            self._updating_size = False

    def _on_height_change(self, event):
        """Handle height change - update width to preserve aspect ratio."""
        if self._updating_size:
            return
        self._updating_size = True
        try:
            aspect_ratio = self._get_aspect_ratio()
            new_height = self.height_spin.GetValue()
            new_width = int(new_height * aspect_ratio)
            self.width_spin.SetValue(max(100, min(7680, new_width)))
        finally:
            self._updating_size = False

    def _update_custom_resolution_state(self):
        """Enable/disable custom resolution and scale inputs based on selection."""
        resolution_idx = self.resolution_choice.GetSelection()
        is_custom = resolution_idx == 5  # Custom option
        is_fit_design = resolution_idx == 1  # Fit Design option

        # Show/hide scale multiplier (only for Fit Design)
        self.scale_label.Enable(is_fit_design)
        self.scale_choice.Enable(is_fit_design)

        # Padding only works with Fit Design (adds equal padding from all sides)
        self.padding_spin.Enable(is_fit_design)

        # Show/hide custom resolution inputs
        self.width_spin.Enable(is_custom)
        self.height_spin.Enable(is_custom)

    def _get_scale_multiplier(self):
        """Get the scale multiplier value from dropdown."""
        scale_map = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 8, 7: 10}
        return scale_map.get(self.scale_choice.GetSelection(), 1)

    def _on_resolution_change(self, event):
        """Handle resolution choice change."""
        self._update_custom_resolution_state()

    def _update_duration(self):
        """Update the duration display based on current speed and stitch range."""
        speed = self.speed_spin.GetValue()
        from_stitch = self.from_stitch_spin.GetValue()
        to_stitch = self.to_stitch_spin.GetValue()
        stitch_count = max(1, to_stitch - from_stitch + 1)

        if speed > 0:
            duration_seconds = stitch_count / speed
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            self.duration_text.SetLabel(f"{minutes}:{seconds:02d}")
        else:
            self.duration_text.SetLabel("--:--")

    def _on_speed_change(self, event):
        """Handle speed change."""
        self._update_duration()

    def _on_range_change(self, event):
        """Handle stitch range change."""
        self._update_duration()

    def _on_export(self, event):
        """Handle export button click."""
        # Get format selection
        format_idx = self.format_choice.GetSelection()
        if format_idx == 0:  # GIF
            wildcard = "GIF files (*.gif)|*.gif"
            default_ext = ".gif"
        else:  # WebP
            wildcard = "WebP files (*.webp)|*.webp"
            default_ext = ".webp"

        # Generate default filename with resolution info
        resolution_idx = self.resolution_choice.GetSelection()
        if resolution_idx == 0:  # Current Size
            width, height = self.drawing_panel.GetClientSize()
        elif resolution_idx == 1:  # Fit Design with scale
            scale = self._get_scale_multiplier()
            padding = self.padding_spin.GetValue()
            width = int(self.drawing_panel.width * scale) + 2 * padding
            height = int(self.drawing_panel.height * scale) + 2 * padding
        elif resolution_idx == 2:  # 720p
            width, height = 1280, 720
        elif resolution_idx == 3:  # 1080p
            width, height = 1920, 1080
        elif resolution_idx == 4:  # 4K
            width, height = 3840, 2160
        else:  # Custom
            width, height = self.width_spin.GetValue(), self.height_spin.GetValue()

        resolution_str = f"{width}x{height}"

        if self.document_name:
            default_filename = f"{self.document_name}_{resolution_str}{default_ext}"
        else:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            default_filename = f"embroidery_animation_{resolution_str}_{timestamp}{default_ext}"

        with wx.FileDialog(
            self, _("Save Video As"), defaultFile=default_filename, wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            output_path = file_dialog.GetPath()
            if not output_path.lower().endswith(default_ext):
                output_path += default_ext

        # Start export in background thread
        self._start_export(output_path)

    def _start_export(self, output_path):
        """Start the export process in a background thread."""
        self.exporting = True
        self.export_btn.Disable()
        self.progress_bar.SetValue(0)
        self.progress_bar.Show()
        self.status_text.SetLabel(_("Preparing export..."))
        self.Layout()

        speed = self.speed_spin.GetValue()
        fps = self.fps_spin.GetValue()
        format_idx = self.format_choice.GetSelection()
        resolution_idx = self.resolution_choice.GetSelection()

        # Determine output size
        if resolution_idx == 0:  # Current Size
            width, height = self.drawing_panel.GetClientSize()
        elif resolution_idx == 1:  # Fit Design with scale
            scale = self._get_scale_multiplier()
            padding = self.padding_spin.GetValue()
            width = int(self.drawing_panel.width * scale) + 2 * padding
            height = int(self.drawing_panel.height * scale) + 2 * padding
        elif resolution_idx == 2:  # 720p
            width, height = 1280, 720
        elif resolution_idx == 3:  # 1080p
            width, height = 1920, 1080
        elif resolution_idx == 4:  # 4K
            width, height = 3840, 2160
        else:  # Custom
            width, height = self.width_spin.GetValue(), self.height_spin.GetValue()

        # Get stitch range
        from_stitch = self.from_stitch_spin.GetValue()
        to_stitch = self.to_stitch_spin.GetValue()

        # Get display options
        show_crosshair = self.crosshair_check.GetValue()
        show_needle_points = self.needle_points_check.GetValue()
        padding = self.padding_spin.GetValue()

        self.export_thread = threading.Thread(
            target=self._export_worker,
            args=(output_path, speed, fps, format_idx, width, height, from_stitch, to_stitch, show_crosshair, show_needle_points, padding),
        )
        self.export_thread.start()

    def _export_worker(self, output_path, speed, fps, format_idx, width, height, from_stitch, to_stitch, show_crosshair, show_needle_points, padding):
        """Worker thread for video export."""
        try:
            from .video_exporter import export_video

            def progress_callback(progress, total, status, frame_current=0, frame_total=0):
                wx.CallAfter(self._update_progress, progress, total, status, frame_current, frame_total)

            export_video(
                drawing_panel=self.drawing_panel,
                output_path=output_path,
                from_stitch=from_stitch,
                to_stitch=to_stitch,
                speed=speed,
                fps=fps,
                width=width,
                height=height,
                background_color=self.background_color,
                progress_callback=progress_callback,
                show_crosshair=show_crosshair,
                show_needle_points=show_needle_points,
                padding=padding,
            )

            wx.CallAfter(self._export_complete, True, output_path)

        except Exception as e:
            wx.CallAfter(self._export_complete, False, str(e))

    def _update_progress(self, progress, total, status, frame_current=0, frame_total=0):
        """Update progress bar (called from main thread)."""
        self.progress_bar.SetValue(progress)
        if status == "encoding":
            self.status_text.SetLabel(_("Encoding video... (50-100%)"))
        elif status == "complete":
            self.status_text.SetLabel(_("Export complete!"))
        else:
            self.status_text.SetLabel(_("Capturing frame %d of %d... (%d%%)") % (frame_current, frame_total, progress))

    def _export_complete(self, success, result):
        """Handle export completion (called from main thread)."""
        self.exporting = False
        self.export_btn.Enable()
        self.progress_bar.SetValue(100 if success else 0)

        if success:
            self.status_text.SetLabel(_("Export complete!"))
            wx.MessageBox(_("Video exported successfully to:\n%s") % result, _("Export Complete"), wx.OK | wx.ICON_INFORMATION)
            self.Close()
        else:
            self.status_text.SetLabel(_("Export failed: %s") % result)
            wx.MessageBox(_("Export failed:\n%s") % result, _("Export Error"), wx.OK | wx.ICON_ERROR)

    def _on_close(self, event):
        """Handle dialog close."""
        if self.exporting:
            # TODO: Add cancellation support
            wx.MessageBox(_("Please wait for export to complete."), _("Export in Progress"), wx.OK | wx.ICON_WARNING)
            return
        event.Skip()
