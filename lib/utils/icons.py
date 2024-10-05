import os

import wx

from .paths import get_resource_dir


def is_dark_theme():
    return wx.SystemSettings().GetAppearance().IsDark()


def load_icon(icon_name, window=None, width=None, height=None):
    if window is None and not (width and height):
        raise ValueError("load_icon(): must pass a window or width and height")

    icon = wx.Image(os.path.join(get_resource_dir("icons"), f"{icon_name}.png"))

    if not (width and height):
        render = wx.RendererNative.Get()
        width = height = render.GetHeaderButtonHeight(window)
    icon.Rescale(width, height, wx.IMAGE_QUALITY_HIGH)

    if is_dark_theme():
        # only way I've found to get a negative image
        data = icon.GetDataBuffer()
        for i in range(len(data)):
            data[i] = 255 - data[i]

    return icon.ConvertToBitmap()
