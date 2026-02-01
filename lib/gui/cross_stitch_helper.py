from math import sqrt

import wx

from ..elements.fill_stitch import FillStitch
from ..extensions.utils.bitmap_to_cross_stitch import BitmapToCrossStitch
from ..i18n import _
from ..utils.settings import global_settings


class CrossStitchHelperFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop("settings")
        self.default_settings = self.settings.copy()
        self.image = kwargs.pop("image")
        self.palette = kwargs.pop("palette")
        wx.Frame.__init__(self, None, wx.ID_ANY, _("Ink/Stitch - Cross stitch"), *args, **kwargs)

        self.SetWindowStyle(wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.widgets_and_panels()
        self.apply_global_settings()
        self.update()
        self.enable_bitmap_settings()
        self.update_color_selection_method()
        self.Show()

    def apply_global_settings(self):
        self.x_only_checkbox.SetValue(global_settings['square'])
        self.box_x.SetValue(global_settings['cross_helper_box_x'])
        self.box_y.SetValue(global_settings['cross_helper_box_y'])
        self.set_params.SetValue(global_settings['cross_helper_set_params'])
        cross_method = self.cross_stitch_method.FindString(self.cross_stitch_options[global_settings['cross_helper_cross_method']])
        self.cross_stitch_method.SetSelection(cross_method)
        self.pixelize.SetValue(global_settings['cross_helper_pixelize'])
        self.pixelize_combined.SetValue(global_settings['cross_helper_pixelize_combined'])
        self.nodes.SetValue(global_settings['cross_helper_nodes'])
        self.coverage.SetValue(global_settings['cross_helper_coverage'])
        self.grid_offset.SetValue(global_settings['cross_helper_grid_offset'])
        self.align_with_canvas.SetValue(global_settings['cross_helper_align_with_canvas'])
        self.setup_grid.SetValue(global_settings['cross_helper_set_grid'])
        self.grid_color.SetColour(wx.Colour(global_settings['cross_helper_grid_color']))
        self.remove_grids.SetValue(global_settings['cross_helper_remove_grids'])
        self.convert_bitmap.SetValue(global_settings['cross_helper_convert_bitmap'])
        self.color_selection_method.SetSelection(global_settings['cross_helper_color_method'])
        self.num_colors.SetValue(global_settings['cross_bitmap_num_colors'])
        self.quantize_method.SetSelection(global_settings['cross_bitmap_quantize_method'])
        self.rgb_color_list.SetValue(global_settings['cross_bitmap_rgb_colors'])
        self.gimp_palette.SetPath(global_settings['cross_bitmap_gimp_palette'])
        self.saturation.SetValue(int(global_settings['cross_bitmap_saturation'] * 100))
        self.brightness.SetValue(int(global_settings['cross_bitmap_brightness'] * 100))
        self.contrast.SetValue(int(global_settings['cross_bitmap_contrast'] * 100))
        self.background_color.SetColour(wx.Colour(global_settings['cross_bitmap_background_color']))
        self.remove_background.SetSelection(global_settings['cross_bitmap_remove_background'])

    def widgets_and_panels(self):
        self.main_panel = wx.Panel(self, wx.ID_ANY)

        notebook_sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = wx.Notebook(self.main_panel, wx.ID_ANY)
        notebook_sizer.Add(self.notebook, 1, wx.EXPAND, 0)

        self.settings_panel = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.settings_panel, _("Settings"))

        # settings
        settings_main_sizer = wx.BoxSizer(wx.VERTICAL)
        settings_options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_settings_sizer = wx.BoxSizer(wx.VERTICAL)
        apply_settings_sizer = wx.BoxSizer(wx.VERTICAL)

        grid_sizer = wx.FlexGridSizer(4, 2, 15, 20)
        grid_sizer.AddGrowableCol(1)

        grid_settings_label = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Grid Settings"))
        font = wx.Font(wx.FontInfo().Bold())
        grid_settings_label.SetFont(font)

        x_only_label = wx.StaticText(self.settings_panel, label=_("Square grid"))
        self.x_only_checkbox = wx.CheckBox(self.settings_panel)
        self.x_only_checkbox.SetValue(True)
        self.x_only_checkbox.Bind(wx.EVT_CHECKBOX, self.update)

        box_x_label = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Grid horizontal spacing (mm)"))
        self.box_x = wx.SpinCtrlDouble(self.settings_panel, value='3', min=0.5, max=100, initial=3, inc=0.1)
        self.box_x.SetDigits(2)
        self.box_x.Bind(wx.EVT_SPINCTRLDOUBLE, self.update)

        self.box_y_label = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Grid vertical spacing (mm)"))
        self.box_y = wx.SpinCtrlDouble(self.settings_panel, value='3', min=0.5, max=100, initial=3, inc=0.1)
        self.box_y.SetDigits(2)
        self.box_y.Bind(wx.EVT_SPINCTRLDOUBLE, self.update)

        self.stitch_length_label = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Stitch length:"))
        self.stitch_length = wx.SpinCtrlDouble(self.settings_panel, value='3', min=0.1, max=100, initial=4.24, inc=0.1)
        self.stitch_length.SetDigits(2)
        self.stitch_length.Bind(wx.EVT_SPINCTRLDOUBLE, self.update_by_stitch_length)

        grid_sizer.AddMany([
            (x_only_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.x_only_checkbox, 1, wx.EXPAND),
            (box_x_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.box_x, 1, wx.EXPAND),
            (self.box_y_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.box_y, 1, wx.EXPAND),
            (self.stitch_length_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.stitch_length, 1, wx.EXPAND)
        ])

        # Pixelate and Param settings
        param_settings_headline = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Params, pixelate and bitmap settings"))
        param_settings_headline.SetFont(font)

        param_settings_sizer = wx.FlexGridSizer(4, 2, 15, 20)
        param_settings_sizer.AddGrowableCol(1)

        self.cross_stitch_options = {p.id: p.name for p in FillStitch.cross_stitch_options}
        cross_stitch_method_label = wx.StaticText(self.settings_panel, label=_("Cross stitch method"))
        self.cross_stitch_method = wx.Choice(self.settings_panel, choices=list(self.cross_stitch_options.values()))

        coverage_label = wx.StaticText(self.settings_panel, label=_("Fill coverage (%)"))
        self.coverage = wx.SpinCtrl(self.settings_panel, wx.ID_ANY, min=0, max=100, initial=50)

        align_with_canvas_label = wx.StaticText(self.settings_panel, label=_("Align with canvas"))
        self.align_with_canvas = wx.CheckBox(self.settings_panel)

        grid_offset_label = wx.StaticText(self.settings_panel, label=_("Grid offset (mm) x[ y]"))
        self.grid_offset = wx.TextCtrl(self.settings_panel, wx.ID_ANY)

        param_settings_sizer.AddMany([
            (cross_stitch_method_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.cross_stitch_method, 1, wx.EXPAND),
            (coverage_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.coverage, 1, wx.EXPAND),
            (align_with_canvas_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.align_with_canvas, 1, wx.EXPAND),
            (grid_offset_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.grid_offset, 1, wx.EXPAND)
        ])

        # Apply grid to
        apply_to_settings = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Apply grid settings to"))
        apply_to_settings.SetFont(font)

        apply_to_grid_sizer = wx.FlexGridSizer(4, 2, 15, 20)
        apply_to_grid_sizer.AddGrowableCol(1)
        apply_page_grid = wx.FlexGridSizer(3, 2, 15, 20)
        apply_page_grid.AddGrowableCol(1)

        set_params_label = wx.StaticText(self.settings_panel, label=_("Params (selected elements)"))
        self.set_params = wx.CheckBox(self.settings_panel)
        self.set_params.Bind(wx.EVT_CHECKBOX, self.update)

        pixelize_label = wx.StaticText(self.settings_panel, label=_("Pixelate (selected elements)"))
        self.pixelize = wx.CheckBox(self.settings_panel)
        self.pixelize.Bind(wx.EVT_CHECKBOX, self.update)

        pixelize_combined_label_text = "     " + _("Avoid overlapping shapes")
        self.pixelize_combined_label = wx.StaticText(self.settings_panel, label=pixelize_combined_label_text)
        self.pixelize_combined = wx.CheckBox(self.settings_panel)
        pixelize_combined_tooltip = _("Inserts a new set of shapes and removes selected elements")
        self.pixelize_combined_label.SetToolTip(pixelize_combined_tooltip)
        self.pixelize_combined.SetToolTip(pixelize_combined_tooltip)

        node_label_text = "     " + _("Add nodes")
        self.nodes_label = wx.StaticText(self.settings_panel, label=node_label_text)
        self.nodes = wx.CheckBox(self.settings_panel)
        nodes_tooltip = _("Add nodes at the horizontal grid spacing value")
        self.nodes_label.SetToolTip(nodes_tooltip)
        self.nodes.SetToolTip(nodes_tooltip)

        apply_to_grid_sizer.AddMany([
            (set_params_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.set_params, 1, wx.EXPAND),
            (pixelize_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.pixelize, 1, wx.EXPAND),
            (self.pixelize_combined_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.pixelize_combined, 1, wx.EXPAND),
            (self.nodes_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.nodes, 1, wx.EXPAND),
        ])

        grid_setup_headline = wx.StaticText(self.settings_panel, wx.ID_ANY, _("Setup page grid"))
        grid_setup_headline.SetFont(font)

        setup_grid_label = wx.StaticText(self.settings_panel, label=_("Page grid"))
        self.setup_grid = wx.CheckBox(self.settings_panel)
        self.setup_grid.Bind(wx.EVT_CHECKBOX, self.update)

        grid_color_label_text = "     " + _("Grid color")
        self.grid_color_label = wx.StaticText(self.settings_panel, label=grid_color_label_text)
        self.grid_color = wx.ColourPickerCtrl(self.settings_panel, colour=wx.Colour('#00d9e5'))

        remove_grids_label_text = "     " + _("Remove previous")
        self.remove_grids_label = wx.StaticText(self.settings_panel, label=remove_grids_label_text)
        self.remove_grids = wx.CheckBox(self.settings_panel)
        remove_grids_tooltip = _("Remove previous cross stitch page grids")
        self.remove_grids_label.SetToolTip(remove_grids_tooltip)
        self.remove_grids.SetToolTip(remove_grids_tooltip)

        grid_settings_sizer.Add(grid_settings_label, 0, wx.EXPAND | wx.ALL, 5)
        grid_settings_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        grid_settings_sizer.Add((30, 30), 0, 0, 0)
        grid_settings_sizer.Add(param_settings_headline, 0, wx.EXPAND | wx.ALL, 5)
        grid_settings_sizer.Add(param_settings_sizer, 1, wx.EXPAND | wx.ALL, 10)

        apply_page_grid.AddMany([
            (setup_grid_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.setup_grid, 1, wx.EXPAND),
            (self.grid_color_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.grid_color, 1, wx.EXPAND),
            (self.remove_grids_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.remove_grids, 1, wx.EXPAND)
        ])

        apply_settings_sizer.Add(apply_to_settings, 0, wx.EXPAND | wx.ALL, 5)
        apply_settings_sizer.Add(apply_to_grid_sizer, 0, wx.EXPAND | wx.ALL, 10)
        apply_settings_sizer.Add(grid_setup_headline, 0, wx.EXPAND | wx.ALL, 10)
        apply_settings_sizer.Add(apply_page_grid, 1, wx.EXPAND | wx.ALL, 10)

        settings_options_sizer.Add(grid_settings_sizer, 1, wx.ALL, 20)
        settings_options_sizer.Add(wx.StaticLine(self.settings_panel, 2, style=wx.LI_VERTICAL), 0, wx.ALL | wx.EXPAND, 20)
        settings_options_sizer.Add(apply_settings_sizer, 1, wx.ALL, 20)

        settings_main_sizer.Add(settings_options_sizer, 1, wx.ALL, 10)

        # image conversion
        self.bitmap = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.bitmap, _("Bitmap Settings"))

        self.bitmap_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.bitmap_sizer = wx.BoxSizer(wx.VERTICAL)

        bitmap_headline = wx.StaticText(self.bitmap, wx.ID_ANY, _("Convert bitmaps to pixelated fill areas"))
        bitmap_headline.SetFont(font)

        bitmap_grid_sizer = wx.FlexGridSizer(11, 2, 15, 20)
        bitmap_grid_sizer.AddGrowableCol(1)

        convert_bitmap_label = wx.StaticText(self.bitmap, label=_("Convert bitmaps"))
        self.convert_bitmap = wx.CheckBox(self.bitmap)
        self.convert_bitmap.Bind(wx.EVT_CHECKBOX, self.enable_bitmap_settings)

        color_choices = [
            _("Number of colors"),
            _("Selected stroke colors"),
            _("List with RGB values"),
            _("GIMP color palette")
        ]
        self.color_selection_method_label = wx.StaticText(self.bitmap, label=_("Color selection"))
        self.color_selection_method = wx.Choice(self.bitmap, choices=color_choices)
        self.color_selection_method.Bind(wx.EVT_CHOICE, self.update_color_selection_method)

        self.num_colors_label = wx.StaticText(self.bitmap, label=_("Number of colors"))
        self.num_colors = wx.SpinCtrl(self.bitmap, wx.ID_ANY, min=1, max=100, initial=5)
        num_color_tooltip = _("Reduces colors to given value.\n"
                              "This may not match the final number of colors. "
                              "It is possible, that colors get removed when the image gets pixelated.")
        self.num_colors_label.SetToolTip(num_color_tooltip)
        self.num_colors.SetToolTip(num_color_tooltip)
        self.num_colors.Bind(wx.EVT_SPINCTRL, self.update_bitmap_panel)

        self.rgb_color_list_label = wx.StaticText(self.bitmap, label=_("RGB value list"))
        self.rgb_color_list = wx.TextCtrl(self.bitmap, wx.ID_ANY)
        rgb_color_tooltip = _("A comma separated list with rgb values: r g b, r, g, b\n"
                              "r,g and b can take a value from 0 - 255")
        self.rgb_color_list_label.SetToolTip(rgb_color_tooltip)
        self.rgb_color_list.SetToolTip(rgb_color_tooltip)
        self.rgb_color_list.Bind(wx.EVT_TEXT, self.update_bitmap_panel)

        self.gimp_palette_label = wx.StaticText(self.bitmap, label=_("Gimp palette file"))
        self.gimp_palette = wx.FilePickerCtrl(self.bitmap, message=_("Select a Gimp palette file"), wildcard="GIMP palette files (*.gpl)|*.gpl")
        gimp_palette_tooltip = _("Restricted to the first 256 colors. Please use a color reduced palette.")
        self.gimp_palette_label.SetToolTip(gimp_palette_tooltip)
        self.gimp_palette.SetToolTip(gimp_palette_tooltip)
        self.gimp_palette.Bind(wx.EVT_FILEPICKER_CHANGED, self.update_bitmap_panel)

        self.quantize_method_label = wx.StaticText(self.bitmap, label=_("Color reduction method"))
        self.quantize_method = wx.Choice(self.bitmap, choices=[_("Median cut"), _("Maxcoverage"), _("Fastoctree")])
        self.quantize_method.Bind(wx.EVT_CHOICE, self.update_bitmap_panel)

        saturation_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.saturation_label = wx.StaticText(self.bitmap, label=_("Saturation"))
        self.saturation = wx.Slider(self.bitmap, value=100, minValue=0, maxValue=200, size=(300, 0))
        self.saturation.SetTick(100)
        self.saturation_numerical_input = wx.SpinCtrlDouble(self.bitmap, value='1', min=0, max=2, initial=1, inc=0.01)
        self.saturation.Bind(wx.EVT_SCROLL, lambda event: self.on_color_slider_change("saturation", event))
        self.saturation_numerical_input.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_numerical_color_change("saturation", event))
        saturation_sizer.Add(self.saturation, 0, wx.ALL | wx.EXPAND, 5)
        saturation_sizer.Add(self.saturation_numerical_input, 0, wx.ALL, 5)

        brightness_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.brightness_label = wx.StaticText(self.bitmap, label=_("Brightness"))
        self.brightness = wx.Slider(self.bitmap, value=100, minValue=0, maxValue=200, size=(300, 0))
        self.brightness.SetTick(100)
        self.brightness_numerical_input = wx.SpinCtrlDouble(self.bitmap, value='1', min=0, max=2, initial=1, inc=0.01)
        self.brightness.Bind(wx.EVT_SCROLL, lambda event: self.on_color_slider_change("brightness", event))
        self.brightness_numerical_input.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_numerical_color_change("brightness", event))
        brightness_sizer.Add(self.brightness, 0, wx.ALL | wx.EXPAND, 5)
        brightness_sizer.Add(self.brightness_numerical_input, 0, wx.ALL, 5)

        contrast_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.contrast_label = wx.StaticText(self.bitmap, label=_("Contrast"))
        self.contrast = wx.Slider(self.bitmap, value=100, minValue=0, maxValue=200, size=(300, 0))
        self.contrast.SetTick(100)
        self.contrast_numerical_input = wx.SpinCtrlDouble(self.bitmap, value='1', min=0, max=2, initial=1, inc=0.01)
        self.contrast.Bind(wx.EVT_SCROLL, lambda event: self.on_color_slider_change("contrast", event))
        self.contrast_numerical_input.Bind(wx.EVT_SPINCTRLDOUBLE, lambda event: self.on_numerical_color_change("contrast", event))
        contrast_sizer.Add(self.contrast, 0, wx.ALL | wx.EXPAND, 5)
        contrast_sizer.Add(self.contrast_numerical_input, 0, wx.ALL, 5)

        background_tooltip_text = _("Background color for transparent images and background removal.")
        self.background_color_label = wx.StaticText(self.bitmap, label=_("Background color"))
        self.background_color_label.SetToolTip(background_tooltip_text)
        self.background_color = wx.ColourPickerCtrl(self.bitmap, colour=wx.BLACK)
        self.background_color.SetToolTip(background_tooltip_text)
        self.background_color.Bind(wx.EVT_COLOURPICKER_CHANGED, self.update_bitmap_panel)

        self.remove_background_label = wx.StaticText(self.bitmap, label=_("Remove background"))
        self.remove_background = wx.Choice(
            self.bitmap,
            choices=[_("Keep background"), _("Remove nearest to background color"), _("Remove most common color")]
        )
        remove_background_tooltip_text = _("Removes the background color.")
        self.remove_background_label.SetToolTip(remove_background_tooltip_text)
        self.remove_background.SetToolTip(remove_background_tooltip_text)
        self.remove_background.Bind(wx.EVT_CHOICE, self.update_bitmap_panel)

        bitmap_grid_sizer.AddMany([
            (convert_bitmap_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.convert_bitmap, 1, wx.EXPAND),
            (self.color_selection_method_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.color_selection_method, 1, wx.EXPAND),
            (self.num_colors_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.num_colors, 1, wx.EXPAND),
            (self.rgb_color_list_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.rgb_color_list, 1, wx.EXPAND),
            (self.gimp_palette_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.gimp_palette, 1, wx.EXPAND),
            (self.quantize_method_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.quantize_method, 1, wx.EXPAND),
            (self.saturation_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (saturation_sizer, 1, wx.EXPAND),
            (self.brightness_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (brightness_sizer, 1, wx.EXPAND),
            (self.contrast_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (contrast_sizer, 1, wx.EXPAND),
            (self.background_color_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.background_color, 1, wx.EXPAND),
            (self.remove_background_label, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.remove_background, 1, wx.EXPAND),
        ])

        bitmap_panel = wx.Panel(self.bitmap, style=wx.BORDER_THEME)
        bitmap_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cross_bitmap = None
        if self.image:
            self.staticbitmap = wx.StaticBitmap(bitmap_panel, size=(500, 700))
            self.cross_bitmap = BitmapToCrossStitch(None, self.image, self.settings, self.palette)
            self.staticbitmap.SetToolTip(_("Preview image (not pixelated)"))
            bitmap_sizer.Add(self.staticbitmap, 0, wx.ALL, 0)
        else:
            no_image_info = wx.StaticText(bitmap_panel, label=_("No image selected"))
            no_image_info.SetForegroundColour(wx.RED)
            bitmap_sizer.Add(no_image_info, 1, wx.ALL | wx.EXPAND, 20)
        bitmap_panel.SetSizer(bitmap_sizer)

        self.bitmap_sizer.Add(bitmap_headline, 0, wx.TOP | wx.LEFT, 20)
        self.bitmap_sizer.Add(bitmap_grid_sizer, 1, wx.EXPAND | wx.ALL, 20)
        self.bitmap_wrapper_sizer.Add(self.bitmap_sizer, 0, wx.ALL, 20)
        self.bitmap_wrapper_sizer.Add(bitmap_panel, 0, wx.ALL | wx.ALIGN_TOP, 20)

        # help
        self.help = wx.Panel(self.notebook, wx.ID_ANY)
        self.notebook.AddPage(self.help, _("Help"))

        help_sizer = wx.BoxSizer(wx.VERTICAL)

        help_text = wx.StaticText(
            self.help,
            wx.ID_ANY,
            _("This extension helps to generate cross stitches in Ink/Stitch. It can:\n\n"
              "* Calculate stitch length for given grid spacing values\n"
              "* Apply cross stitch parameters to selected fill elements.\n"
              "* Pixelate outlines of selected fill elements.\n"
              "* Generate pixelated fills from bitmaps.\n"
              "* Apply spacing values to page grid."),
            style=wx.ALIGN_LEFT
        )
        help_text.Wrap(500)
        help_sizer.Add(help_text, 0, wx.TOP | wx.LEFT | wx.RIGHT, 20)

        help_sizer.Add((20, 20), 0, 0, 0)

        website_info = wx.StaticText(self.help, wx.ID_ANY, _("More information on our website:"))
        help_sizer.Add(website_info, 0, wx.TOP | wx.LEFT | wx.RIGHT, 20)

        self.website_link = wx.adv.HyperlinkCtrl(
            self.help,
            wx.ID_ANY,
            _("https://inkstitch.org/docs/tools-fill/#cross-stitch"),
            _("https://inkstitch.org/docs/tools-fill/#cross-stitch")
        )
        help_sizer.Add(self.website_link, 0, wx.BOTTOM | wx.LEFT | wx.RIGHT, 20)

        # apply or cancel
        apply_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.reset_button = wx.Button(self.main_panel, label=_("Reset values"))
        self.reset_button.Bind(wx.EVT_BUTTON, self.reset_values)
        self.cancel_button = wx.Button(self.main_panel, label=_("Cancel"))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
        self.apply_button = wx.Button(self.main_panel, label=_("Apply"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.apply)
        apply_sizer.Add(self.reset_button, 0, wx.RIGHT | wx.LEFT | wx.BOTTOM, 10)
        apply_sizer.AddStretchSpacer(prop=1)
        apply_sizer.Add(self.cancel_button, 0, wx.RIGHT | wx.BOTTOM, 10)
        apply_sizer.Add(self.apply_button, 0, wx.RIGHT | wx.BOTTOM, 10)

        notebook_sizer.Add(apply_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # set sizers
        self.settings_panel.SetSizer(settings_main_sizer)
        self.bitmap.SetSizer(self.bitmap_wrapper_sizer)
        self.help.SetSizer(help_sizer)

        self.main_panel.SetSizerAndFit(notebook_sizer)
        self.Fit()
        self.Layout()

    def update_by_stitch_length(self, event=None):
        stitch_length = self.stitch_length.GetValue()
        xy = stitch_length / sqrt(2)
        self.box_x.SetValue(xy)
        self.box_y.SetValue(xy)

    def update(self, event=None):
        y_on = not self.x_only_checkbox.GetValue()
        self.box_y.Enable(y_on)
        self.box_y_label.Enable(y_on)

        box_x = self.box_x.GetValue()
        box_y = self.box_y.GetValue()
        if not y_on:
            box_y = box_x
            self.box_y.SetValue(box_y)
        result = sqrt(pow(box_x, 2) + pow(box_y, 2))
        self.stitch_length.SetValue(result)

        if y_on:
            self.stitch_length.Enable(False)
        else:
            self.stitch_length.Enable(True)

        enable = self.pixelize.GetValue()
        self.pixelize_combined_label.Enable(enable)
        self.pixelize_combined.Enable(enable)
        self.nodes_label.Enable(enable)
        self.nodes.Enable(enable)

        self.grid_color_label.Enable(self.setup_grid.GetValue())
        self.grid_color.Enable(self.setup_grid.GetValue())
        self.remove_grids_label.Enable(self.setup_grid.GetValue())
        self.remove_grids.Enable(self.setup_grid.GetValue())

    def on_color_slider_change(self, rule, event):
        # update numberical color values
        if rule == "saturation":
            self.saturation_numerical_input.SetValue(self.saturation.GetValue() / 100)
        elif rule == "brightness":
            self.brightness_numerical_input.SetValue(self.brightness.GetValue() / 100)
        elif rule == "contrast":
            self.contrast_numerical_input.SetValue(self.contrast.GetValue() / 100)
        self.update_bitmap_panel()

    def on_numerical_color_change(self, rule, event):
        if rule == "saturation":
            saturation = self.saturation_numerical_input.GetValue()
            self.saturation.SetValue(int(saturation * 100))
        elif rule == "brightness":
            brightness = self.brightness_numerical_input.GetValue()
            self.brightness.SetValue(int(brightness * 100))
        elif rule == "contrast":
            contrast = self.contrast_numerical_input.GetValue()
            self.contrast.SetValue(int(contrast * 100))
        self.update_bitmap_panel()

    def enable_bitmap_settings(self, event=None):
        convert = self.convert_bitmap.GetValue()
        self.color_selection_method_label.Enable(convert)
        self.color_selection_method.Enable(convert)
        self.num_colors_label.Enable(convert)
        self.num_colors.Enable(convert)
        self.quantize_method_label.Enable(convert)
        self.quantize_method.Enable(convert)
        self.rgb_color_list_label.Enable(convert)
        self.rgb_color_list.Enable(convert)
        self.gimp_palette_label.Enable(convert)
        self.gimp_palette.Enable(convert)
        self.saturation_label.Enable(convert)
        self.saturation.Enable(convert)
        self.saturation_numerical_input.Enable(convert)
        self.brightness_label.Enable(convert)
        self.brightness.Enable(convert)
        self.brightness_numerical_input.Enable(convert)
        self.contrast_label.Enable(convert)
        self.contrast.Enable(convert)
        self.contrast_numerical_input.Enable(convert)
        self.background_color_label.Enable(convert)
        self.background_color.Enable(convert)
        self.remove_background_label.Enable(convert)
        self.remove_background.Enable(convert)

    def update_color_selection_method(self, event=None):
        method = self.color_selection_method.GetSelection()
        self.num_colors_label.Show(method == 0)
        self.num_colors.Show(method == 0)
        self.quantize_method_label.Show(method == 0)
        self.quantize_method.Show(method == 0)

        self.rgb_color_list_label.Show(method == 2)
        self.rgb_color_list.Show(method == 2)

        self.gimp_palette_label.Show(method == 3)
        self.gimp_palette.Show(method == 3)

        self.bitmap.Fit()
        self.bitmap.Layout()
        self.update_bitmap_panel()

    def update_bitmap_panel(self, event=None):
        if self.image:
            self.apply_settings()
            self.update_image()

    def update_image(self):
        if self.image is None or self.cross_bitmap.original_image is None:
            return
        self.cross_bitmap.apply_color_corrections()
        cross_bitmap = self.cross_bitmap.reduced_image
        cross_bitmap = self.cross_bitmap.apply_transform(cross_bitmap)
        cross_bitmap = self.cross_bitmap.apply_clip(cross_bitmap)
        width, height = cross_bitmap.size
        width, height = self.scale_bitmap(cross_bitmap, width, height, 400)
        height, width = self.scale_bitmap(cross_bitmap, height, width, 600)
        cross_bitmap = cross_bitmap.resize((width, height))
        bitmap_prev = wx.Bitmap.FromBufferRGBA(width, height, cross_bitmap.tobytes())
        self.staticbitmap.SetBitmap(bitmap_prev)

    def scale_bitmap(self, bitmap, a, b, max_size):
        # scale bitmap and preserve aspect ratio
        if a > max_size:
            b = int(b / (a / max_size))
            a = max_size
        return a, b

    def reset_values(self, event):
        self.box_x.SetValue(self.default_settings['box_x'])
        self.box_y.SetValue(self.default_settings['box_y'])
        cross_method = self.cross_stitch_method.FindString(self.cross_stitch_options[self.default_settings['cross_method']])
        self.color_selection_method.SetSelection(cross_method)
        self.coverage.SetValue(self.default_settings['coverage'])
        self.grid_offset.SetValue(self.default_settings['grid_offset'])
        self.align_with_canvas.SetValue(self.default_settings['align_with_canvas'])
        self.grid_color.SetColour(wx.Colour(self.default_settings['grid_color']))
        self.num_colors.SetValue(self.default_settings['bitmap_num_colors'])
        self.quantize_method.SetSelection(self.default_settings['bitmap_quantize_method'])
        self.brightness.SetValue(int(self.default_settings['bitmap_brightness'] * 100))
        self.contrast.SetValue(int(self.default_settings['bitmap_contrast'] * 100))
        self.saturation.SetValue(int(self.default_settings['bitmap_saturation'] * 100))
        self.rgb_color_list.SetValue(self.default_settings['bitmap_rgb_colors'])
        self.gimp_palette.SetPath(self.default_settings['bitmap_gimp_palette'])
        self.background_color.SetColour(wx.Colour(self.default_settings['bitmap_background_color']))
        self.remove_background.SetSelection(self.default_settings['bitmap_remove_background'])
        self.update()
        self.update_color_selection_method()
        self.apply_settings()

    def apply_settings(self):
        self.settings['square'] = self.x_only_checkbox.GetValue()
        self.settings['box_x'] = self.box_x.GetValue()
        self.settings['box_y'] = self.box_y.GetValue()
        self.settings['set_params'] = self.set_params.GetValue()
        self.settings['cross_method'] = self.get_cross_method()
        self.settings['pixelize'] = self.pixelize.GetValue()
        self.settings['pixelize_combined'] = self.pixelize_combined.GetValue()
        self.settings['nodes'] = self.nodes.GetValue()
        self.settings['coverage'] = self.coverage.GetValue()
        self.settings['grid_offset'] = self.grid_offset.GetValue()
        self.settings['align_with_canvas'] = self.align_with_canvas.GetValue()
        self.settings['set_grid'] = self.setup_grid.GetValue()
        self.settings['grid_color'] = self.grid_color.GetColour().Get(False)
        self.settings['remove_grids'] = self.remove_grids.GetValue()
        self.settings['color_method'] = self.color_selection_method.GetSelection()
        self.settings['convert_bitmap'] = self.convert_bitmap.GetValue()
        self.settings['bitmap_num_colors'] = self.num_colors.GetValue()
        self.settings['bitmap_quantize_method'] = self.quantize_method.GetSelection()
        self.settings['bitmap_brightness'] = self.brightness.GetValue() / 100
        self.settings['bitmap_contrast'] = self.contrast.GetValue() / 100
        self.settings['bitmap_saturation'] = self.saturation.GetValue() / 100
        self.settings['bitmap_rgb_colors'] = self.rgb_color_list.GetValue()
        self.settings['bitmap_gimp_palette'] = self.gimp_palette.GetPath()
        self.settings['bitmap_background_color'] = self.background_color.GetColour().Get(False)
        self.settings['bitmap_remove_background'] = self.remove_background.GetSelection()

    def get_cross_method(self):
        current_cross_method = self.cross_stitch_method.GetString(self.cross_stitch_method.GetSelection())
        return [method_id for method_id, method in self.cross_stitch_options.items() if method == current_cross_method][0]

    def apply(self, event):
        self.settings['applied'] = True
        self.apply_settings()

        global_settings['square'] = self.x_only_checkbox.GetValue()
        global_settings['cross_helper_box_x'] = self.box_x.GetValue()
        global_settings['cross_helper_box_y'] = self.box_y.GetValue()
        global_settings['cross_helper_set_params'] = self.set_params.GetValue()
        global_settings['cross_helper_cross_method'] = self.get_cross_method()
        global_settings['cross_helper_pixelize'] = self.pixelize.GetValue()
        global_settings['cross_helper_pixelize_combined'] = self.pixelize_combined.GetValue()
        global_settings['cross_helper_nodes'] = self.nodes.GetValue()
        global_settings['cross_helper_coverage'] = self.coverage.GetValue()
        global_settings['cross_helper_grid_offset'] = self.grid_offset.GetValue()
        global_settings['cross_helper_align_with_canvas'] = self.align_with_canvas.GetValue()
        global_settings['cross_helper_set_grid'] = self.setup_grid.GetValue()
        global_settings['cross_helper_grid_color'] = self.grid_color.GetColour().Get(False)
        global_settings['cross_helper_remove_grids'] = self.remove_grids.GetValue()
        global_settings['cross_helper_convert_bitmap'] = self.convert_bitmap.GetValue()
        global_settings['cross_helper_color_method'] = self.color_selection_method.GetSelection()
        global_settings['cross_bitmap_num_colors'] = self.num_colors.GetValue()
        global_settings['cross_bitmap_quantize_method'] = self.quantize_method.GetSelection()
        global_settings['cross_bitmap_saturation'] = self.saturation.GetValue() / 100
        global_settings['cross_bitmap_brightness'] = self.brightness.GetValue() / 100
        global_settings['cross_bitmap_contrast'] = self.contrast.GetValue() / 100
        global_settings['cross_bitmap_rgb_colors'] = self.rgb_color_list.GetValue()
        global_settings['cross_bitmap_gimp_palette'] = self.gimp_palette.GetPath()
        global_settings['cross_bitmap_background_color'] = self.background_color.GetColour().Get(False)
        global_settings['cross_bitmap_remove_background'] = self.remove_background.GetSelection()

        self.GetTopLevelParent().Close()
        return

    def cancel(self, event=None):
        self.Destroy()


class CrossStitchHelperApp(wx.App):
    def __init__(self, settings, image, palette):
        self.settings = settings
        self.image = image
        self.palette = palette
        super().__init__()

    def OnInit(self):
        frame = CrossStitchHelperFrame(settings=self.settings, image=self.image, palette=self.palette)
        self.SetTopWindow(frame)
        frame.Show()
        return True
