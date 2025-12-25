from math import sqrt

import wx

from ..i18n import _


class CalcuatorFrame(wx.Frame):
    def __init__(self, parent, title):
        super(CalcuatorFrame, self).__init__(parent, title=title)
        self.widgets()
        self.Show()

    # Declare a function to add new buttons, icons, etc. to our app
    def widgets(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.FlexGridSizer(4, 2, 10, 10)
        grid_sizer.AddGrowableCol(1)

        x_only_label = wx.StaticText(self, label=_("Square grid"))
        self.x_only_checkbox = wx.CheckBox(self)
        self.x_only_checkbox.SetValue(True)
        self.x_only_checkbox.Bind(wx.EVT_CHECKBOX, self.update)

        box_x_label = wx.StaticText(self, wx.ID_ANY, _("Grid width (mm)"))
        self.box_x = wx.SpinCtrlDouble(self, value='3', min=0.5, max=100, initial=3, inc=1)
        self.box_x.Bind(wx.EVT_SPINCTRLDOUBLE, self.update)

        self.box_y_label = wx.StaticText(self, wx.ID_ANY, _("Grid geight (mm)"))
        self.box_y = wx.SpinCtrlDouble(self, value='3', min=0.5, max=100, initial=3, inc=1)
        self.box_y.Bind(wx.EVT_SPINCTRLDOUBLE, self.update)

        result_label = wx.StaticText(self, wx.ID_ANY, _("Stitch_length:"))
        self.result = wx.StaticText(self, wx.ID_ANY, label='')

        grid_sizer.AddMany([
            (x_only_label),
            (self.x_only_checkbox, 1, wx.EXPAND),
            (box_x_label),
            (self.box_x, 1, wx.EXPAND),
            (self.box_y_label),
            (self.box_y, 1, wx.EXPAND),
            (result_label),
            (self.result, 1, wx.EXPAND)
        ])

        self.update()

        main_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(main_sizer)

    def update(self, event=None):
        y_on = not self.x_only_checkbox.GetValue()
        self.box_y.Enable(y_on)
        self.box_y_label.Enable(y_on)
        box_x = self.box_x.GetValue()
        if y_on:
            box_y = self.box_y.GetValue()
        else:
            box_y = box_x
        result = sqrt(pow(box_x, 2) + pow(box_y, 2))
        self.result.SetLabel("{:.2f}".format(result))


class CrossStitchCalculatorApp(wx.App):
    def OnInit(self):
        frame = CalcuatorFrame(None, "Cross Stitch: stitch length calculator")
        self.SetTopWindow(frame)
        frame.Show()
        return True
