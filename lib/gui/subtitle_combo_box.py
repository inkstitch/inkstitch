import wx
import wx.adv
from wx.lib.wordwrap import wordwrap


class SubtitleComboBox(wx.adv.OwnerDrawnComboBox):
    TITLE_FONT_SIZE = 12
    SUBTITLE_FONT_SIZE = 10

    # I'd love to make this 12 too, but if I do it seems to get drawn as 10
    # initially no matter what I do.
    CONTROL_FONT_SIZE = 12

    MARGIN = 5

    def __init__(self, *args, **kwargs):
        self.titles = kwargs.get('choices', [])
        subtitles = kwargs.pop('subtitles', {})
        self.subtitles = [subtitles.get(title, '') for title in self.titles]
        wx.adv.OwnerDrawnComboBox.__init__(self, *args, **kwargs)

        self.control_font = wx.Font(pointSize=self.CONTROL_FONT_SIZE, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)
        self.title_font = wx.Font(pointSize=self.TITLE_FONT_SIZE, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)
        self.subtitle_font = wx.Font(pointSize=self.SUBTITLE_FONT_SIZE, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)

    def OnMeasureItemWidth(self, item):
        # This _should_ allow us to set the width of the combobox to match the
        # width of the widest title.  In reality, this method is never called
        # and I can't figure out why.  We just use self.GetSize().GetWidth()
        # instead and rely on the parent window to size us appropriately.  Ugh.

        title = self.titles[item]

        # technique from https://stackoverflow.com/a/23529463/4249120
        dc = wx.ScreenDC()
        dc.SetFont(self.title_font)

        return dc.GetTextExtent(title).GetWidth() + 2 * self.MARGIN

    def OnMeasureItem(self, item):
        title = self.titles[item]
        subtitle = self.subtitles[item]

        dc = wx.ScreenDC()
        dc.SetFont(self.subtitle_font)
        wrapped = wordwrap(subtitle, self.GetSize().GetWidth(), dc)
        subtitle_height = dc.GetTextExtent(wrapped).GetHeight()

        dc = wx.ScreenDC()
        dc.SetFont(self.title_font)
        title_height = dc.GetTextExtent(title).GetHeight()

        return subtitle_height + title_height + 3 * self.MARGIN

    def OnDrawBackground(self, dc, rect, item, flags):
        if flags & wx.adv.ODCB_PAINTING_SELECTED:
            # let the parent class draw the selected item so we don't
            # hae to figure out the highlight color
            wx.adv.OwnerDrawnComboBox.OnDrawBackground(self, dc, rect, item, flags)
        else:
            # alternate white and grey for the dropdown items, and draw the
            # combo box itself as white
            if flags & wx.adv.ODCB_PAINTING_CONTROL or item % 2 == 0:
                background_color = wx.Colour(255, 255, 255)
            else:
                background_color = wx.Colour(240, 240, 240)

            dc.SetBrush(wx.Brush(background_color))
            dc.SetPen(wx.Pen(background_color))
            dc.DrawRectangle(rect)

    def OnDrawItem(self, dc, rect, item, flags):
        if flags & wx.adv.ODCB_PAINTING_CONTROL:
            # painting the selected item in the box
            dc.SetFont(self.control_font)
            dc.DrawText(self.titles[item], rect.x + self.MARGIN, rect.y + self.MARGIN)
        else:
            # painting the items in the popup
            dc.SetFont(self.title_font)
            title_height = dc.GetCharHeight()
            dc.DrawText(self.titles[item], rect.x + self.MARGIN, rect.y + self.MARGIN)

            dc.SetFont(self.subtitle_font)
            subtitle = wordwrap(self.subtitles[item], self.GetSize().GetWidth(), dc)
            dc.DrawText(subtitle, rect.x + self.MARGIN, rect.y + title_height + self.MARGIN * 2)
