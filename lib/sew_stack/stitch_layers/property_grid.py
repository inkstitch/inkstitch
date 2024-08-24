import re

import wx.html
import wx.propgrid

from ...debug.debug import debug
from ...svg import PIXELS_PER_MM


class CheckBoxProperty(wx.propgrid.BoolProperty):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetAttribute(wx.propgrid.PG_BOOL_USE_CHECKBOX, True)


class MillimeterFloatProperty(wx.propgrid.FloatProperty):
    def DoGetEditorClass(self):
        return wx.propgrid.PGEditor_SpinCtrl

    def ValueToString(self, value, flags=None):
        # Goal: present "0.25 mm" to the user but still let them edit the number
        # as a plain float using the SpinCtrl.
        #
        # This code was determined by experimentation.  I can't find this
        # behavior described anywhere in the docs for wxPython or wxWidgets.
        # Note that even though flags is a bitmask, == seems to be correct here.
        #  Using & results in subtly different behavior that doesn't look right.
        if flags == wx.propgrid.PG_VALUE_IS_CURRENT:
            return f"{value:0.2f} mm"
        else:
            return f"{value:0.2f}"

    def GetValue(self):
        return self.m_value * PIXELS_PER_MM


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
        self.layer = None
        self.pg = None

    def generate(self, layer, pg):
        self.layer = layer
        self.pg = pg
        root_category = self.pg.GetRoot()
        for child in self._children:
            child.generate(self.layer, self.pg, root_category)

        return self.pg


class Category:
    def __init__(self, label, name=wx.propgrid.PG_LABEL):
        self.name = name
        self.label = label
        self._children = []
        self.category = None
        self.layer = None
        self.pg = None

    def children(self, *args):
        self._children = args
        return self

    def generate(self, layer, pg, parent):
        self.layer = layer
        self.pg = pg
        self.category = wx.propgrid.PropertyCategory(
            name=self.name, label=self.label)
        pg.AppendIn(parent, self.category)

        for child in self._children:
            child.generate(layer, pg, self.category)


class Property:
    # Adapted from wxPython source
    _type_to_property = {
        str: wx.propgrid.StringProperty,
        int: wx.propgrid.IntProperty,
        float: MillimeterFloatProperty,
        bool: CheckBoxProperty,
        list: wx.propgrid.ArrayStringProperty,
        tuple: wx.propgrid.ArrayStringProperty,
        wx.Colour: wx.propgrid.ColourProperty
    }

    def __init__(self, name, label, help="", default=None, min=None, max=None, **kwargs):
        self.name = name
        self.label = label
        self.help = help
        self.default = default
        self.min = min
        self.max = max
        self.attributes = kwargs
        self.property = None
        self.layer = None
        self.pg = None

    def generate(self, layer, pg, parent):
        self.layer = layer
        self.pg = pg

        value = layer.config.get(self.name, self.default)
        property_class = self.get_property_class(type(value))

        self.property = property_class(name=self.name, label=self.label, value=value)
        pg.AppendIn(parent, self.property)
        pg.SetPropertyHelpString(self.property, self.help)
        for name, value in self.attributes.items():
            self.property.SetAttribute(name.title(), value)

    def get_property_class(self, data_type):
        try:
            return self._type_to_property[data_type]
        except KeyError:
            return wx.propgrid.IntProperty


class SewStackPropertyGrid(wx.propgrid.PropertyGrid):
    # Without this override, selecting a property will cause its help text to
    # be shown in the status bar.  We use the status bar for the simulator,
    # so we don't want PropertyGrid to overwrite it.
    def GetStatusBar(self):
        return None


class PropertyGridMixin:
    def __init__(self, *args, **kwargs):
        self.property_grid = None
        self.help_box = None
        self.property_grid_panel = None

        super().__init__(*args, **kwargs)

    @classmethod
    @property
    def properties(cls):
        """Define PropertyGrid properties and attributes concisely

        Return value:
            an instance of Properties

        Example:
            return Properties(...)
        """
        raise NotImplementedError(
            f"{cls.__name__} must implement properties() with @classmethod and @property decorators!")

    def get_panel(self, parent):
        if self.property_grid_panel is None:
            self.property_grid_panel = wx.Panel(parent, wx.ID_ANY)
            sizer = wx.BoxSizer(wx.VERTICAL)

            self.property_grid = SewStackPropertyGrid(
                self.property_grid_panel,
                wx.ID_ANY,
                style=wx.propgrid.PG_SPLITTER_AUTO_CENTER | wx.propgrid.PG_BOLD_MODIFIED | wx.propgrid.PG_DESCRIPTION
            )
            # self.property_grid.SetColumnCount(3)
            self.properties.generate(self, self.property_grid)
            self.property_grid.ResetColumnSizes(enableAutoResizing=True)
            self.property_grid.Bind(wx.propgrid.EVT_PG_CHANGED, self.on_property_changed)
            self.property_grid.Bind(wx.propgrid.EVT_PG_SELECTED, self.on_select)

            self.help_box = wx.html.HtmlWindow(self.property_grid_panel, wx.ID_ANY, style=wx.html.HW_SCROLLBAR_AUTO)

            sizer.Add(self.property_grid, 2, wx.EXPAND | wx.TOP, 10)
            sizer.Add(self.help_box, 1, wx.EXPAND | wx.TOP, 2)
            self.property_grid_panel.SetSizer(sizer)
            sizer.Layout()

        return self.property_grid_panel

    def on_property_changed(self, event):
        # override in subclass if needed but always call super().on_property_changed(event)!
        changed_property = event.GetProperty()
        self.config[changed_property.GetName()] = changed_property.GetValue()
        debug.log(
            f"Changed property: {changed_property.GetName()} = {changed_property.GetValue()}")

    def on_select(self, event):
        property = event.GetProperty()

        if property:
            self.help_box.SetPage(self.format_help(property))
        else:
            self.help_box.SetPage("")

    def format_help(self, property):
        help_string = f"<h2>{property.GetLabel()}</h2>"
        help_string += re.sub(r'\n\n?', "<br/>", property.GetHelpString())

        return help_string
