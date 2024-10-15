import wx


class SimpleBox(wx.Panel):
    """Draw a box around one window.

    Usage:

        window = SomeWindow(your_window_or_panel, wx.ID_ANY)
        box = SimpleBox(your_window_or_panel, window)
        some_sizer.Add(box, ...)

    """

    def __init__(self, parent, window, *args, width=1, radius=2, **kwargs):
        super().__init__(parent, wx.ID_ANY, *args, **kwargs)

        window.Reparent(self)
        self.window = window
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(window, 1, wx.EXPAND | wx.ALL, 2)
        self.SetSizer(self.sizer)

        self.width = width
        self.radius = radius

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)

    def on_erase_background(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
        size = self.GetClientSize()

        if wx.SystemSettings().GetAppearance().IsDark():
            dc.SetPen(wx.Pen(wx.Colour(32, 32, 32), width=self.width))
        else:
            dc.SetPen(wx.Pen(wx.Colour(128, 128, 128), width=self.width))

        dc.SetBrush(wx.NullBrush)
        dc.DrawRoundedRectangle(0, 0, size.x, size.y, self.radius)
