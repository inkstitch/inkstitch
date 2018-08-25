import sys
import os
from os.path import dirname, realpath
import gettext

_ = translation = None
locale_dir = None

# Use N_ to mark a string for translation but _not_ immediately translate it.
# reference: https://docs.python.org/3/library/gettext.html#deferred-translations
# Makefile configures pybabel to treat N_() the same as _()


def N_(message): return message


def _set_locale_dir():
    global locale_dir

    if getattr(sys, 'frozen', False):
        # we are in a pyinstaller installation
        locale_dir = sys._MEIPASS
    else:
        locale_dir = dirname(dirname(realpath(__file__)))

    locale_dir = os.path.join(locale_dir, 'locales')


def localize(languages=None):
    global translation, _

    translation = gettext.translation("inkstitch", locale_dir, fallback=True)
    _ = translation.gettext


_set_locale_dir()
localize()
