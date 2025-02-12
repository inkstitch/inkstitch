import wx


class PromptingComboBox(wx.ComboBox):
    def __init__(self, parent, choices=[], style=0, **kwargs):
        if choices is None:
            choices = []
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, style=style, choices=choices, **kwargs)
        self.choices = choices
        self.Bind(wx.EVT_KEY_DOWN, self.on_button_down)
        self.Bind(wx.EVT_TEXT, self.on_text_edit)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_edit)
        self.ignore_text_event = False
        self.delete_key = False
        self.found_choice = False
        self.parent = parent

    def update_choices(self, choices):
        self.choices = choices

    def on_button_down(self, event):
        if event.GetKeyCode() == 8:
            self.delete_key = True
        event.Skip()

    def on_text_edit(self, event):
        current_text = event.GetString()
        if len(current_text) == 0 or current_text == " ":
            self.delete_key = False
            self.parent.on_combobox_change(event)
            return
        if self.ignore_text_event:
            self.ignore_text_event = False
            return
        if self.delete_key:
            self.delete_key = False
            if self.found_choice:
                current_text = current_text[:-1]

        self.found_choice = False
        for i, choice in enumerate(self.choices):
            if choice.startswith(current_text.strip()):
                self.ignore_text_event = True
                self.SetValue(choice)
                self.SetInsertionPoint(len(current_text))
                self.SetTextSelection(len(current_text), len(choice))
                self.found_choice = True
                self.parent.on_combobox_change(event)
                break
