import wx
from wx.lib.mixins.listctrl import TextEditMixin  # type: ignore[import-untyped]


class EditableListCtrl(wx.ListCtrl, TextEditMixin):

    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, editable_column=2):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        TextEditMixin.__init__(self)
        self.editable_column = editable_column

    def OpenEditor(self, column, row):
        self.original_data = self.GetItemText(row, column)
        if column == self.editable_column:
            TextEditMixin.OpenEditor(self, column, row)
        if self.editable_column == 3 and column == 0:
            self.CheckItem(row, not self.IsItemChecked(row))
        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_escape)

    def on_escape(self, event=None):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.CloseEditor(event=None, swap=True)
        event.Skip()

    def CloseEditor(self, event=None, swap=False):
        text = self.editor.GetValue()
        if swap:
            self.editor.Hide()
            TextEditMixin.CloseEditor(self, event)
            return

        if text:
            try:
                float(text)
            except ValueError:
                swap = True

            if swap:
                self.editor.SetValue(self.original_data)

        TextEditMixin.CloseEditor(self, event)
