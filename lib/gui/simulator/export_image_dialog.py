# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

"""Dialog for exporting embroidery simulation as image."""

import time

import wx

from ...i18n import _


class ExportImageDialog(wx.Dialog):
    """Dialog for exporting embroidery simulation as image."""

    # Frame selection options
    FRAME_CURRENT = 0
    FRAME_LAST = 1
    FRAME_SPECIFIC = 2

    def __init__(self, parent, drawing_panel, num_stitches, current_stitch, background_color, document_name="", **kwargs):
        """Initialize the export image dialog.

        Args:
            parent: Parent window
            drawing_panel: The DrawingPanel instance for frame capture
            num_stitches: Total number of stitches in the design
            current_stitch: Current stitch position in simulator
            background_color: Current background color from simulator
            document_name: Optional name of the document for default filename
        """
        super().__init__(parent, title=_("Export Simulation Image"), **kwargs)

        self.drawing_panel = drawing_panel
        self.num_stitches = num_stitches
        self.current_stitch = current_stitch
        self.background_color = background_color
        self.document_name = document_name

        self._create_ui()
        self._bind_events()
        self._update_stitch_spin_state()

        self.SetMinSize((400, 380))
        self.Fit()
        self.Centre()

    def _create_ui(self):
        """Create the dialog UI elements."""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Frame selection
        frame_box = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Frame Selection")), wx.VERTICAL)

        self.frame_choice = wx.RadioBox(
            self,
            choices=[_("Current Frame (stitch %d)") % self.current_stitch, _("Last Frame (stitch %d)") % self.num_stitches, _("Specific Stitch")],
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS,
        )
        frame_box.Add(self.frame_choice, 0, wx.EXPAND | wx.ALL, 5)

        # Specific stitch input
        stitch_sizer = wx.BoxSizer(wx.HORIZONTAL)
        stitch_label = wx.StaticText(self, label=_("Stitch Number:"))
        self.stitch_spin = wx.SpinCtrl(self, value=str(self.current_stitch), min=1, max=self.num_stitches, initial=self.current_stitch)
        stitch_sizer.Add(stitch_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        stitch_sizer.Add(self.stitch_spin, 1, wx.EXPAND)
        frame_box.Add(stitch_sizer, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(frame_box, 0, wx.EXPAND | wx.ALL, 10)

        # Format selection
        format_box = wx.StaticBoxSizer(wx.StaticBox(self, label=_("Export Settings")), wx.VERTICAL)

        format_sizer = wx.BoxSizer(wx.HORIZONTAL)
        format_label = wx.StaticText(self, label=_("Format:"))
        self.format_choice = wx.Choice(self, choices=["PNG", "PNG (Transparent)", "JPEG"])
        self.format_choice.SetSelection(0)
        format_sizer.Add(format_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        format_sizer.Add(self.format_choice, 1, wx.EXPAND)
        format_box.Add(format_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Resolution selection
        resolution_sizer = wx.BoxSizer(wx.HORIZONTAL)
        resolution_label = wx.StaticText(self, label=_("Resolution:"))
        self.resolution_choice = wx.Choice(
            self, choices=[_("Current Size"), _("Fit Design"), "720p (1280x720)", "1080p (1920x1080)", "4K (3840x2160)", _("Custom")]
        )
        self.resolution_choice.SetSelection(0)
        resolution_sizer.Add(resolution_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        resolution_sizer.Add(self.resolution_choice, 1, wx.EXPAND)
        format_box.Add(resolution_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Scale multiplier for Fit Design (1x to 10x)
        scale_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scale_label = wx.StaticText(self, label=_("Scale Multiplier:"))
        self.scale_choice = wx.Choice(self, choices=["1x", "2x", "3x", "4x", "5x", "6x", "8x", "10x"])
        self.scale_choice.SetSelection(0)  # Default 1x
        scale_sizer.Add(self.scale_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        scale_sizer.Add(self.scale_choice, 1, wx.EXPAND)
        format_box.Add(scale_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Custom resolution inputs
        custom_res_sizer = wx.BoxSizer(wx.HORIZONTAL)
        custom_res_sizer.Add(wx.StaticText(self, label=_("Width:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.width_spin = wx.SpinCtrl(self, value="1920", min=100, max=7680, initial=1920)
        custom_res_sizer.Add(self.width_spin, 1, wx.EXPAND | wx.RIGHT, 10)
        custom_res_sizer.Add(wx.StaticText(self, label=_("Height:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.height_spin = wx.SpinCtrl(self, value="1080", min=100, max=4320, initial=1080)
        custom_res_sizer.Add(self.height_spin, 1, wx.EXPAND)
        format_box.Add(custom_res_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Padding input
        padding_sizer = wx.BoxSizer(wx.HORIZONTAL)
        padding_sizer.Add(wx.StaticText(self, label=_("Padding (px):")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        self.padding_spin = wx.SpinCtrl(self, value="20", min=0, max=200, initial=20)
        padding_sizer.Add(self.padding_spin, 1, wx.EXPAND)
        format_box.Add(padding_sizer, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(format_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

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

        # Buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.export_btn = wx.Button(self, label=_("Export"))
        self.cancel_btn = wx.Button(self, wx.ID_CANCEL, label=_("Cancel"))
        button_sizer.Add(self.export_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.cancel_btn, 0, wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(main_sizer)
        self._update_custom_resolution_state()

    def _bind_events(self):
        """Bind event handlers."""
        self.frame_choice.Bind(wx.EVT_RADIOBOX, self._on_frame_choice_change)
        self.resolution_choice.Bind(wx.EVT_CHOICE, self._on_resolution_change)
        self.width_spin.Bind(wx.EVT_SPINCTRL, self._on_width_change)
        self.height_spin.Bind(wx.EVT_SPINCTRL, self._on_height_change)
        self.export_btn.Bind(wx.EVT_BUTTON, self._on_export)

        # Track if we're updating to prevent recursive calls
        self._updating_size = False

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

    def _update_stitch_spin_state(self):
        """Enable/disable stitch spin based on frame selection."""
        selection = self.frame_choice.GetSelection()
        self.stitch_spin.Enable(selection == self.FRAME_SPECIFIC)

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

    def _on_frame_choice_change(self, event):
        """Handle frame choice change."""
        self._update_stitch_spin_state()

    def _on_resolution_change(self, event):
        """Handle resolution choice change."""
        self._update_custom_resolution_state()

    def _get_target_stitch(self):
        """Get the target stitch number based on selection."""
        selection = self.frame_choice.GetSelection()
        if selection == self.FRAME_CURRENT:
            return self.current_stitch
        elif selection == self.FRAME_LAST:
            return self.num_stitches
        else:
            return self.stitch_spin.GetValue()

    def _get_scale_multiplier(self):
        """Get the scale multiplier value from dropdown."""
        scale_map = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 8, 7: 10}
        return scale_map.get(self.scale_choice.GetSelection(), 1)

    def _get_output_size(self, include_padding=False):
        """Get output width and height based on selection.

        Args:
            include_padding: If True, add padding to Fit Design dimensions
        """
        resolution_idx = self.resolution_choice.GetSelection()
        if resolution_idx == 0:  # Current Size
            return self.drawing_panel.GetClientSize()
        elif resolution_idx == 1:  # Fit Design with scale multiplier
            scale = self._get_scale_multiplier()
            padding = self.padding_spin.GetValue() if include_padding else 0
            width = int(self.drawing_panel.width * scale) + 2 * padding
            height = int(self.drawing_panel.height * scale) + 2 * padding
            return width, height
        elif resolution_idx == 2:  # 720p
            return 1280, 720
        elif resolution_idx == 3:  # 1080p
            return 1920, 1080
        elif resolution_idx == 4:  # 4K
            return 3840, 2160
        else:  # Custom
            return self.width_spin.GetValue(), self.height_spin.GetValue()

    def _on_export(self, event):
        """Handle export button click."""
        format_idx = self.format_choice.GetSelection()
        # 0 = PNG, 1 = PNG Transparent, 2 = JPEG
        if format_idx in (0, 1):
            wildcard = "PNG files (*.png)|*.png"
            default_ext = ".png"
        else:
            wildcard = "JPEG files (*.jpg)|*.jpg"
            default_ext = ".jpg"

        # Generate default filename with stitch number and resolution
        stitch_num = self._get_target_stitch()
        width, height = self._get_output_size(include_padding=True)
        resolution_str = f"{width}x{height}"
        transparent_str = "_transparent" if format_idx == 1 else ""

        if self.document_name:
            default_filename = f"{self.document_name}_stitch{stitch_num}_{resolution_str}{transparent_str}{default_ext}"
        else:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            default_filename = f"embroidery_stitch{stitch_num}_{resolution_str}{transparent_str}_{timestamp}{default_ext}"

        with wx.FileDialog(
            self, _("Save Image As"), defaultFile=default_filename, wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            output_path = file_dialog.GetPath()
            if not output_path.lower().endswith(default_ext):
                output_path += default_ext

        # Export the image
        self._export_image(output_path, format_idx)

    def _export_image(self, output_path, format_idx):
        """Export the image."""
        try:
            from .video_exporter import capture_frame, bitmap_to_pil_image

            # Determine output size (include padding for Fit Design mode)
            width, height = self._get_output_size(include_padding=True)

            # Get target stitch
            stitch_index = self._get_target_stitch()

            # Determine if transparent
            transparent = format_idx == 1

            # Get display options
            show_crosshair = self.crosshair_check.GetValue()
            show_needle_points = self.needle_points_check.GetValue()
            padding = self.padding_spin.GetValue()

            # Capture frame with display options
            bitmap = capture_frame(
                self.drawing_panel, stitch_index, width, height, self.background_color, transparent, show_crosshair, show_needle_points, padding
            )

            # Convert and save
            pil_image = bitmap_to_pil_image(bitmap)

            if format_idx in (0, 1):  # PNG or PNG Transparent
                # Save with 300 DPI (pHYs metadata: 11811 pixels per meter = 300 DPI)
                pil_image.save(output_path, "PNG", dpi=(300, 300))
            else:  # JPEG
                # Convert RGBA to RGB for JPEG
                if pil_image.mode == "RGBA":
                    pil_image = pil_image.convert("RGB")
                pil_image.save(output_path, "JPEG", quality=95, dpi=(300, 300))

            wx.MessageBox(_("Image exported successfully to:\n%s") % output_path, _("Export Complete"), wx.OK | wx.ICON_INFORMATION)
            self.Close()

        except Exception as e:
            wx.MessageBox(_("Export failed:\n%s") % str(e), _("Export Error"), wx.OK | wx.ICON_ERROR)
