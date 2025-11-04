import re
from typing import Callable

import wx.html
import wx.propgrid

from ...debug.debug import debug
from ...gui.windows import SimpleBox
from ...i18n import _
from ...utils.classproperty import classproperty
from ...utils.settings import global_settings


class CheckBoxProperty(wx.propgrid.BoolProperty):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetAttribute(wx.propgrid.PG_BOOL_USE_CHECKBOX, True)


class InkStitchNumericProperty:
    """Base class for functionality common to Ink/Stitch-specific numeric PropertyGrid Properties.

    When using this class, be sure to specify it first in the inheritance list.
    This is necessary because wxPython's property classes don't properly call
    the super-class's constructor.
    """

    # typing hints for PyCharm
    value_to_string: Callable
    IsValueUnspecified: Callable
    GetAttribute: Callable
    SetValueInEvent: Callable

    def __init__(self, *args, prefix="", unit="", **kwargs):
        super().__init__(*args, **kwargs)

        self.prefix = prefix
        self.unit = unit

    def set_unit(self, unit):
        self.unit = unit

    def set_prefix(self, prefix):
        self.prefix = prefix

    def DoGetEditorClass(self):
        return wx.propgrid.PGEditor_SpinCtrl

    def ValueToString(self, value, flags=None):
        # Goal: present "0.25 mm" (for example) to the user but still let them
        # edit the number using the SpinCtrl.
        #
        # This code was determined by experimentation.  I can't find this
        # behavior described anywhere in the docs for wxPython or wxWidgets.
        # Note that even though flags is a bitmask, == seems to be correct here.
        # Using & results in subtly different behavior that doesn't look right.

        value_str = self.value_to_string(value)
        if flags == wx.propgrid.PG_VALUE_IS_CURRENT:
            prefix = ""
            if self.prefix:
                prefix = self.prefix + " "

            return f"{prefix}{value_str} {self.unit}"
        else:
            return value_str

    def OnEvent(self, pg, window, event):
        # If the user starts editing a property that had multiple values, set
        # the value quickly before editing starts.  Otherwise, clicking the
        # spin-buttons causes a low-level C++ exception since the property is
        # set to None.
        if event.GetEventType() == wx.wxEVT_CHILD_FOCUS:
            if self.IsValueUnspecified():
                self.SetValueInEvent(self.GetAttribute('InitialValue'))
                return True

        return False


class InkStitchFloatProperty(InkStitchNumericProperty, wx.propgrid.FloatProperty):
    def __init__(self, *args, prefix="", unit="", **kwargs):
        super().__init__(*args, **kwargs)

        # default to a step of 0.1, but can be changed per-property
        self.SetAttribute(wx.propgrid.PG_ATTR_SPINCTRL_STEP, 0.1)

    def value_to_string(self, value):
        return f"{value:0.2f}"


class InkStitchIntProperty(InkStitchNumericProperty, wx.propgrid.IntProperty):
    def value_to_string(self, value):
        return str(value)


class Properties:
    """Define PropertyGrid properties and attributes concisely

    Example:
        Properties(
            Category("cat1",_("First category")).children(
                Property("stitch_length", _("Running stitch length"),
                    help=_("Distance between stitches"),
                    min=0.1,
                    max=5,
                    unit="mm"
                ),
                Property("repeats", _("Running stitch repeats"),
                    help=...
                ),
                Category("subcat1", _("Subcategory")).children(
                    Property(...),
                    Property(...)
                )
            )
        )
    """

    def __init__(self, *children):
        self._children = children
        self.pg = None

    def generate(self, pg, config):
        self.pg = pg
        root_category = self.pg.GetRoot()
        for child in self._children:
            child.generate(self.pg, root_category, config)

        return self.pg

    def all_properties(self):
        yield from self._iter_properties(self)

    def _iter_properties(self, parent):
        for child in parent._children:
            if isinstance(child, Category):
                yield from self._iter_properties(child)
            else:
                yield child


class Category:
    def __init__(self, label, name=wx.propgrid.PG_LABEL, help=None):
        self.name = name
        self.label = label
        self.help = help
        self._children = []
        self.category = None
        self.pg = None

    def children(self, *args):
        self._children.extend(args)
        return self

    def generate(self, pg, parent, config):
        self.pg = pg
        self.category = wx.propgrid.PropertyCategory(
            name=self.name, label=self.label)
        if self.help:
            pg.SetPropertyHelpString(self.category, self.help)
        pg.AppendIn(parent, self.category)

        for child in self._children:
            child.generate(pg, self.category, config)


class Property:
    # Adapted from wxPython source
    _type_to_property = {
        str: wx.propgrid.StringProperty,
        int: InkStitchIntProperty,
        float: InkStitchFloatProperty,
        bool: CheckBoxProperty,
        list: wx.propgrid.ArrayStringProperty,
        tuple: wx.propgrid.ArrayStringProperty,
        wx.Colour: wx.propgrid.ColourProperty
    }

    def __init__(self, name, label, help="", min=None, max=None, prefix=None, unit=None, type=None, attributes=None):
        self.name = name
        self.label = label
        self.help = help
        self.min = min
        self.max = max
        self.prefix = prefix
        self.unit = unit
        self.type = type
        self.attributes = attributes
        self.property = None
        self.pg = None

    def generate(self, pg, parent, config):
        self.pg = pg

        property_class = self.get_property_class()
        self.property = property_class(name=self.name, label=self.label)
        self.property.SetValue(config.get(self.name))

        pg.AppendIn(parent, self.property)
        if self.help:
            pg.SetPropertyHelpString(self.property, self.help)

        if self.prefix:
            self.property.set_prefix(self.prefix)
        if self.unit:
            self.property.set_unit(self.unit)

        if self.attributes:
            for name, value in self.attributes.items():
                self.property.SetAttribute(name.title(), value)

        # These attributes are provided as convenient shorthands
        if self.max is not None:
            self.property.SetAttribute(wx.propgrid.PG_ATTR_MAX, self.max)
        if self.min is not None:
            self.property.SetAttribute(wx.propgrid.PG_ATTR_MIN, self.min)

    def get_property_class(self):
        if self.type is not None:
            if issubclass(self.type, wx.propgrid.PGProperty):
                return self.type
            elif self.type in self._type_to_property:
                return self._type_to_property[self.type]
            else:
                raise ValueError(f"property type {repr(self.type)} unknown")
        else:
            return InkStitchFloatProperty


class SewStackPropertyGrid(wx.propgrid.PropertyGrid):
    # Without this override, selecting a property will cause its help text to
    # be shown in the status bar.  We use the status bar for the simulator,
    # so we don't want PropertyGrid to overwrite it.
    def GetStatusBar(self):
        return None


class StitchLayerEditor:
    def __init__(self, layers, change_callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hints = {}
        self.initial_values = {}
        self.config = self.merge_config(layers)
        self.defaults = layers[0].defaults
        self.property_grid = None
        self.help_box = None
        self.property_grid_panel = None
        self.change_callback = change_callback

    @classproperty
    def properties(cls):
        """Define PropertyGrid properties and attributes concisely.

        Must be implemented in each child class.  Be sure to include all the
        properties listed in the corresponding StitchLayer subclass's defaults
        property.

        Return value:
            an instance of Properties

        Example:
            return Properties(...)
        """
        raise NotImplementedError(f"{cls.__name__} must implement properties() with @classmethod and @property decorators!")

    def merge_config(self, layers):
        if not layers:
            return {}

        if len(set(type(layer) for layer in layers)) > 1:
            raise ValueError("StitchLayerEditor: internal error: all layers must be of the same type!")

        config = dict(layers[0].defaults)
        for property_name in list(config.keys()):
            # Get all values from layers.  Don't use set() here because values
            # might not be hashable (example: list).
            values = []
            unique_values = []
            for layer in layers:
                value = layer.config[property_name]
                values.append(value)
                if value not in unique_values:
                    unique_values.append(value)

            if len(unique_values) == 1:
                config[property_name] = unique_values[0]
            elif len(unique_values) > 1:
                unique_values.sort(key=lambda item: values.count(item), reverse=True)
                del config[property_name]
                self.hints[property_name] = "[ " + ", ".join(str(value) for value in unique_values) + " ]"
                self.initial_values[property_name] = unique_values[0]

        return config

    def update_layer(self, layer):
        """ Apply only properties modified by the user to layer's config """
        if self.property_grid is not None:
            for property in self.property_grid.Items:
                if isinstance(property, wx.propgrid.PGProperty):
                    if property.HasFlag(wx.propgrid.PG_PROP_MODIFIED):
                        name = property.GetName()
                        value = property.GetValue()
                        layer.config[name] = value

    def has_changes(self):
        if self.property_grid is None:
            return False
        else:
            return any(property.HasFlag(wx.propgrid.PG_PROP_MODIFIED) for property in self.property_grid.Items)

    def get_panel(self, parent):
        if self.property_grid_panel is None:
            self.layer_editor_panel = wx.Panel(parent, wx.ID_ANY)

            main_sizer = wx.BoxSizer(wx.VERTICAL)
            self.splitter = wx.SplitterWindow(self.layer_editor_panel, style=wx.SP_LIVE_UPDATE)
            self.splitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.on_sash_position_changed)

            self.property_grid_panel = wx.Panel(self.splitter, wx.ID_ANY)
            property_grid_sizer = wx.BoxSizer(wx.VERTICAL)
            self.property_grid = SewStackPropertyGrid(
                self.property_grid_panel,
                wx.ID_ANY,
                style=wx.propgrid.PG_SPLITTER_AUTO_CENTER | wx.propgrid.PG_BOLD_MODIFIED | wx.propgrid.PG_DESCRIPTION
            )
            self.properties.generate(self.property_grid, self.config)
            self.property_grid.ResetColumnSizes(enableAutoResizing=True)
            self.property_grid.Bind(wx.propgrid.EVT_PG_CHANGED, self.on_property_changed)
            self.property_grid.Bind(wx.propgrid.EVT_PG_SELECTED, self.on_select)
            self.property_grid_box = SimpleBox(self.property_grid_panel, self.property_grid)

            buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
            buttons_sizer.Add((0, 0), 1, 0, 0)

            self.undo_button = wx.Button(self.property_grid_panel, wx.ID_ANY, style=wx.BU_EXACTFIT)
            self.undo_button.SetBitmapLabel(wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_OTHER))
            self.undo_button.SetToolTip(_("Undo changes"))
            self.undo_button.Disable()
            self.undo_button.Bind(wx.EVT_BUTTON, self.on_undo)
            buttons_sizer.Add(self.undo_button, 0, 0, 0)

            self.reset_button = wx.Button(self.property_grid_panel, wx.ID_ANY, style=wx.BU_EXACTFIT)
            # For some reason wx.ART_REFRESH doesn't exist in wxPython even
            # though wxART_REFRESH does exist in wxWidgets.  Fortunately we
            # can use the string value.
            self.reset_button.SetBitmapLabel(wx.ArtProvider.GetBitmap("wxART_REFRESH", wx.ART_TOOLBAR))
            self.reset_button.SetToolTip(_("Reset to default"))
            self.reset_button.Disable()
            self.reset_button.Bind(wx.EVT_BUTTON, self.on_reset)
            buttons_sizer.Add(self.reset_button, 0, wx.LEFT, 5)

            self.help_panel = wx.Panel(self.splitter, wx.ID_ANY)
            self.help_box = wx.html.HtmlWindow(self.help_panel, wx.ID_ANY, style=wx.html.HW_SCROLLBAR_AUTO)
            self.help_box_box = SimpleBox(self.help_panel, self.help_box)
            help_sizer = wx.BoxSizer(wx.VERTICAL)
            help_sizer.Add(self.help_box_box, 1, wx.EXPAND | wx.TOP, 10)
            self.help_panel.SetSizer(help_sizer)
            self.show_help(self.property_grid.GetFirst(wx.propgrid.PG_ITERATE_CATEGORIES))

            property_grid_sizer.Add(self.property_grid_box, 1, wx.EXPAND | wx.TOP, 10)
            property_grid_sizer.Add(buttons_sizer, 0, wx.EXPAND | wx.TOP, 2)
            property_grid_sizer.Add((0, 0), 0, wx.BOTTOM, 10)
            self.property_grid_panel.SetSizer(property_grid_sizer)

            main_sizer.Add(self.splitter, 1, wx.EXPAND)
            self.layer_editor_panel.SetSizer(main_sizer)
            self.splitter.SplitHorizontally(self.property_grid_panel, self.help_panel, global_settings['stitch_layer_editor_sash_position'])
            self.splitter.SetMinimumPaneSize(1)

            for property_name, hint in self.hints.items():
                if property := self.property_grid.GetPropertyByName(property_name):
                    property.SetAttribute(wx.propgrid.PG_ATTR_HINT, hint)
                    property.SetAttribute("InitialValue", self.initial_values[property_name])

            main_sizer.Layout()

        return self.layer_editor_panel

    def on_property_changed(self, event):
        # override in subclass if needed but always call super().on_property_changed(event)!
        changed_property = event.GetProperty()
        if self.change_callback is not None:
            self.change_callback(changed_property.GetName(), changed_property.GetValue())

        debug.log(f"Changed property: {changed_property.GetName()} = {changed_property.GetValue()}")

    def on_select(self, event):
        property = event.GetProperty()

        if property is None:
            enable = False
        else:
            enable = not property.IsCategory()
            self.show_help(property)

        self.undo_button.Enable(enable)
        self.reset_button.Enable(enable)

    def on_undo(self, event):
        property = self.property_grid.GetSelection()

        if property and not property.IsCategory():
            property_name = property.GetName()
            if property_name in self.config:
                value = self.config[property_name]
                self.property_grid.ChangePropertyValue(property_name, value)
                self.change_callback(property_name, value)
                property.SetModifiedStatus(False)
                self.property_grid.RefreshEditor()

    def on_reset(self, event):
        property = self.property_grid.GetSelection()

        if property and not property.IsCategory():
            property_name = property.GetName()
            if property_name in self.defaults:
                value = self.defaults[property_name]
                self.property_grid.ChangePropertyValue(property_name, value)
                self.change_callback(property_name, value)

                if value == self.config[property_name]:
                    property.SetModifiedStatus(False)

                self.property_grid.RefreshEditor()

    def on_sash_position_changed(self, event):
        global_settings['stitch_layer_editor_sash_position'] = event.GetSashPosition()

    def show_help(self, property):
        if property:
            self.help_box.SetPage(self.format_help(property))
        else:
            self.help_box.SetPage("")

    def format_help(self, property):
        help_string = f"<h2>{property.GetLabel()}</h2>"
        help_string += re.sub(r'\n\n?', "<br/>", property.GetHelpString())

        return help_string
