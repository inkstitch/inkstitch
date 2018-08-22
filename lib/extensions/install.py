# -*- coding: UTF-8 -*-

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

from ..utils import guess_inkscape_config_path, get_bundled_dir


class InstallerFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.path = guess_inkscape_config_path()

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        text_sizer = wx.BoxSizer(wx.HORIZONTAL)

        text = (_('Ink/Stitch can install files ("add-ons") that make it easier to use Inkscape to create machine embroidery designs.  '
                  'These add-ons will be installed:') +
                "\n\n   • " + _("thread manufacturer color palettes") +
                "\n   • " + _("Ink/Stitch visual commands (Object -> Symbols...)"))

        static_text = wx.StaticText(panel, label=text)
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        static_text.SetFont(font)
        text_sizer.Add(static_text, proportion=0, flag=wx.ALL | wx.EXPAND, border=10)
        sizer.Add(text_sizer, proportion=3, flag=wx.ALL | wx.EXPAND, border=0)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        install_button = wx.Button(panel, wx.ID_ANY, _("Install"))
        install_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK))
        buttons_sizer.Add(install_button, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        cancel_button = wx.Button(panel, wx.ID_CANCEL, _("Cancel"))
        buttons_sizer.Add(cancel_button, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        sizer.Add(buttons_sizer, proportion=1, flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)

        panel.SetSizer(sizer)
        panel.Layout()

        cancel_button.Bind(wx.EVT_BUTTON, self.cancel_button_clicked)
        install_button.Bind(wx.EVT_BUTTON, self.install_button_clicked)

    def cancel_button_clicked(self, event):
        self.Destroy()

    def chooser_button_clicked(self, event):
        dialog = wx.DirDialog(self, _("Choose Inkscape directory"))
        if dialog.ShowModal() != wx.ID_CANCEL:
            self.path_input.SetValue(dialog.GetPath())

    def install_button_clicked(self, event):
        try:
            self.install_addons('palettes')
            self.install_addons('symbols')
        except Exception as e:
            wx.MessageDialog(self,
                             _('Inkscape add-on installation failed') + ': \n' + traceback.format_exc(),
                             _('Installation Failed'),
                             wx.OK).ShowModal()
        else:
            wx.MessageDialog(self,
                             _('Inkscape add-on files have been installed.  Please restart Inkscape to load the new add-ons.'),
                             _('Installation Completed'),
                             wx.OK).ShowModal()

        self.Destroy()

    def install_addons(self, type):
        path = os.path.join(self.path, type)
        src_dir = get_bundled_dir(type)
        self.copy_files(glob(os.path.join(src_dir, "*")), path)

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


class Install(inkex.Effect):
    def effect(self):
        app = wx.App()
        installer_frame = InstallerFrame(None, title=_("Ink/Stitch Add-ons Installer"), size=(550, 250))
        installer_frame.Show()
        app.MainLoop()
