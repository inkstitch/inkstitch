import sys
import traceback
import os
from os.path import realpath, dirname
from glob import glob
from threading import Thread
import socket
import errno
import time
import logging
import wx
import inkex
from ..utils import guess_inkscape_config_path


class InstallPalettesFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        default_path = os.path.join(guess_inkscape_config_path(), "palettes")

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        text = wx.StaticText(panel, label=_("Directory in which to install palettes:"))
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        text.SetFont(font)
        sizer.Add(text, proportion=0, flag=wx.ALL|wx.EXPAND, border=10)

        path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.path_input = wx.TextCtrl(panel, wx.ID_ANY, value=default_path)
        path_sizer.Add(self.path_input, proportion=3, flag=wx.RIGHT|wx.EXPAND, border=20)
        chooser_button = wx.Button(panel, wx.ID_OPEN, _('Choose another directory...'))
        path_sizer.Add(chooser_button, proportion=1, flag=wx.EXPAND)
        sizer.Add(path_sizer, proportion=0, flag=wx.ALL|wx.EXPAND, border=10)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        install_button = wx.Button(panel, wx.ID_ANY, _("Install"))
        install_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK))
        buttons_sizer.Add(install_button, proportion=0, flag=wx.ALIGN_RIGHT|wx.ALL, border=5)
        cancel_button = wx.Button(panel, wx.ID_CANCEL, _("Cancel"))
        buttons_sizer.Add(cancel_button, proportion=0, flag=wx.ALIGN_RIGHT|wx.ALL, border=5)
        sizer.Add(buttons_sizer, proportion=0, flag=wx.ALIGN_RIGHT)

        outer_sizer = wx.BoxSizer(wx.HORIZONTAL)
        outer_sizer.Add(sizer, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)

        panel.SetSizer(outer_sizer)
        panel.Layout()

        chooser_button.Bind(wx.EVT_BUTTON, self.chooser_button_clicked)
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel_button_clicked)
        install_button.Bind(wx.EVT_BUTTON, self.install_button_clicked)

    def cancel_button_clicked(self, event):
        self.Destroy()

    def chooser_button_clicked(self, event):
        dialog = wx.DirDialog(self, _("Choose Inkscape palettes directory"))
        if dialog.ShowModal() != wx.ID_CANCEL:
            self.path_input.SetValue(dialog.GetPath())

    def install_button_clicked(self, event):
        try:
            self.install_palettes()
        except Exception, e:
            wx.MessageDialog(self,
                             _('Thread palette installation failed') + ': \n' + traceback.format_exc(),
                             _('Installation Failed'),
                             wx.OK).ShowModal()
        else:
            wx.MessageDialog(self,
                             _('Thread palette files have been installed.  Please restart Inkscape to load the new palettes.'),
                             _('Installation Completed'),
                             wx.OK).ShowModal()

        self.Destroy()

    def install_palettes(self):
        path = self.path_input.GetValue()
        palettes_dir = self.get_bundled_palettes_dir()
        self.copy_files(glob(os.path.join(palettes_dir, "*")), path)

    def get_bundled_palettes_dir(self):
        if getattr(sys, 'frozen', None) is not None:
            return realpath(os.path.join(sys._MEIPASS, '..', 'palettes'))
        else:
            return os.path.join(dirname(realpath(__file__)), 'palettes')

    if (sys.platform == "win32"):
        # If we try to just use shutil.copy it says the operation requires elevation.
        def copy_files(self, files, dest):
            import winutils

            winutils.copy(files, dest)
    else:
        def copy_files(self, files, dest):
            import shutil

            if not os.path.exists(dest):
                os.makedirs(dest)

            for palette_file in files:
                shutil.copy(palette_file, dest)

class Palettes(inkex.Effect):
    def effect(self):
        app = wx.App()
        installer_frame = InstallPalettesFrame(None, title=_("Ink/Stitch Thread Palette Installer"), size=(450, 200))
        installer_frame.Show()
        app.MainLoop()
