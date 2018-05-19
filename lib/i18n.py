import sys
import os
import gettext

_ = translation = None

def localize():
    if getattr(sys, 'frozen', False):
        # we are in a pyinstaller installation
        locale_dir = sys._MEIPASS
    else:
        locale_dir = os.path.dirname(__file__)

    locale_dir = os.path.join(locale_dir, 'locales')

    global translation, _

    translation = gettext.translation("inkstitch", locale_dir, fallback=True)
    _ = translation.gettext

localize()
