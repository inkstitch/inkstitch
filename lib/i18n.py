# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import gettext
import os
from typing import Callable, Tuple

from .utils import cache, get_resource_dir

# Use N_ to mark a string for translation but _not_ immediately translate it.
# reference: https://docs.python.org/3/library/gettext.html#deferred-translations
# Makefile configures pybabel to treat N_() the same as _()


def N_(message: str) -> str:
    return message


def localize(languages=None) -> Tuple[Callable[[str], str], gettext.NullTranslations]:
    locale_dir = get_resource_dir('locales')

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
