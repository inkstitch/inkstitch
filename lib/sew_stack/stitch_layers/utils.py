import re

import wx.propgrid
import wx.html

from ...debug.debug import debug
from ...svg import PIXELS_PER_MM
from ...utils import coordinate_list_to_point_list
from ...utils.dotdict import DotDict


# Functionality for StitchLayers is broken down into separate "mix-in" classes.
# This allows us to divide up the implementation so that we don'd end up with
# one gigantic StitchLayer class.  Individual StitchLayer subclasses can include
# just the functionality they need.
#
# Python multiple inheritance is cool, and as long as we include a super().__init__()
# call in every __init__() method we implement, we'll ensure that all mix-in
# classes' constructors get called.  Skipping implementing the __init__() method in a
# mix-in class is also allowed.

class PathUtilsMixin:
    def __init__(self, *args, **kwargs):
        self.element = kwargs.pop('sew_stack')
        super().__init__(*args, **kwargs)

    @property
    def paths(self):
        return [coordinate_list_to_point_list(path) for path in self.element.paths]

    @property
    def stroke_color(self):
        return self.element.get_style("stroke")

    @property
    def fill_color(self):
        return self.element.get_style("stroke")


class ConfigMixin:
    def __init__(self, *args, **kwargs):
        self.config = DotDict()

        # merge in default configs from all parent and mix-in classes
        for ancestor_class in reversed(self.__class__.__mro__):
            try:
                self.config.update(ancestor_class.DEFAULT_CONFIG)
            except AttributeError:
                # ignore ancestor classes that don't have DEFAULT_CONFIG
                pass

        # now override defaults with the actual config
        self.config.update(kwargs.pop('config'))

        super().__init__(*args, **kwargs)


class RandomizationMixin(PathUtilsMixin, ConfigMixin):
    DEFAULT_CONFIG = dict(
        random_seed=None
    )

    def get_random_seed(self):
        if self.config.random_seed is None:
            self.config.random_seed = self.element.get_default_random_seed() or ""

        return self.config.random_seed


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


class PropertyGridHelper:
    """Define PropertyGrid properties and attributes concisely

    Example:
        PropertyGridHelper(
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

    def __init__(self, name, label, help="", min=None, max=None, **kwargs):
        self.name = name
        self.label = label
        self.help = help
        self.attributes = kwargs
        self.property = None
        self.layer = None
        self.pg = None

    def generate(self, layer, pg, parent):
        self.layer = layer
        self.pg = pg

        value = layer.config.get(self.name)
        property_class = self.get_property_class(type(value))

        self.property = property_class(
            name=self.name, label=self.label, value=value)
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


class PropertyGridMixin(ConfigMixin):
    def __init__(self, *args, **kwargs):
        self.property_grid = None
        self.help_box = None
        self.property_grid_panel = None
        self.extra_config_panel = None

        super().__init__(*args, **kwargs)

    @classmethod
    @property
    def LAYOUT(_class):
        """Define PropertyGrid properties and attributes concisely

        Return value:
            an instance of PropertyGridHelper

        Example:
            return PropertyGridHelper(...)
        """
        raise NotImplementedError(
            f"{_class.__name__} must implement LAYOUT as a class property!")

    def get_property_grid_panel(self, parent):
        if self.property_grid_panel is None:
            self.property_grid_panel = wx.Panel(parent, wx.ID_ANY)
            sizer = wx.BoxSizer(wx.VERTICAL)

            self.property_grid = SewStackPropertyGrid(
                self.property_grid_panel,
                wx.ID_ANY,
                style=wx.propgrid.PG_SPLITTER_AUTO_CENTER | wx.propgrid.PG_BOLD_MODIFIED | wx.propgrid.PG_DESCRIPTION
            )
            # self.property_grid.SetColumnCount(3)
            self.LAYOUT.generate(self, self.property_grid)
            self.property_grid.ResetColumnSizes(enableAutoResizing=True)
            self.property_grid.Bind(wx.propgrid.EVT_PG_CHANGED, self.on_property_changed)
            self.property_grid.Bind(wx.propgrid.EVT_PG_SELECTED, self.on_select)

            self.help_box = wx.html.HtmlWindow(self.property_grid_panel, wx.ID_ANY, style=wx.html.HW_SCROLLBAR_AUTO)

            sizer.Add(self.property_grid, 2, wx.EXPAND | wx.TOP, 10)
            sizer.Add(self.help_box, 1, wx.EXPAND | wx.TOP, 2)
            self.property_grid_panel.SetSizer(sizer)
            sizer.Layout()

        return self.property_grid_panel

    def generate_extra_config_panel(self, parent):
        self.extra_config_panel = wx.Panel(parent, wx.ID_ANY)
        self.populate_extra_config_panel(self.extra_config_panel)

    def populate_extra_config_panel(self, panel):
        # override in subclass to add additional layer configuration UI outside of the
        # PropertyGrid
        pass

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
