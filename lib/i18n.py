# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import gettext
import os
import sys
from os.path import dirname, realpath
from typing import Callable, Tuple

from .utils import cache

# Use N_ to mark a string for translation but _not_ immediately translate it.
# reference: https://docs.python.org/3/library/gettext.html#deferred-translations
# Makefile configures pybabel to treat N_() the same as _()


def N_(message: str) -> str: return message


def localize(languages=None) -> Tuple[Callable[[str], str], gettext.NullTranslations]:
    if getattr(sys, 'frozen', False):
        # we are in a pyinstaller installation
        locale_dir = sys._MEIPASS  # type: ignore[attr-defined]
    else:
        locale_dir = dirname(dirname(realpath(__file__)))

    if sys.platform == "darwin" and getattr(sys, 'frozen', False):
        locale_dir = os.path.join(locale_dir, "..", 'Resources', 'locales')
    else:
        locale_dir = os.path.join(locale_dir, 'locales')

    global translation, _

    translation = gettext.translation("inkstitch", locale_dir, fallback=True)
    _ = translation.gettext
    return (_, translation)


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


_, translation = localize()
