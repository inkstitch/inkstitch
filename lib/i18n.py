import gettext
import os
import sys
from os.path import dirname, realpath

from .utils import cache

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


@cache
def get_languages():
    """return a list of languages configured by the user

    I really wish gettext provided this as a function.  Instead, we've duplicated
    its code below.
    """

    languages = []

    for envar in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
        val = os.environ.get(envar)
        if val:
            languages = val.split(':')
            break

    if 'C' not in languages:
        languages.append('C')

    return languages


_set_locale_dir()
localize()
