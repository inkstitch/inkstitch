# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import atexit
import hashlib
import os
import pickle
import sqlite3
from typing import TypeVar, Callable, Any, cast

import diskcache  # type: ignore[import-untyped]

from lib.utils.settings import global_settings

from .paths import get_user_dir
from functools import lru_cache

# See https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
F = TypeVar('F', bound=Callable[..., Any])


# simplify use of lru_cache decorator
def cache(func: F) -> F:
    return cast(F, lru_cache(maxsize=None)(func))


__stitch_plan_cache = None


def get_stitch_plan_cache():
    global __stitch_plan_cache

    if __stitch_plan_cache is None:
        cache_dir = get_user_dir('cache')
        stitch_plan_dir = os.path.join(cache_dir, 'stitch_plan')
        size_limit = global_settings['cache_size'] * 1024 * 1024
        try:
            __stitch_plan_cache = diskcache.Cache(stitch_plan_dir, size=size_limit)
        except (sqlite3.DatabaseError, sqlite3.OperationalError):
            # reset cache database file if it couldn't parse correctly
            cache_file = os.path.join(stitch_plan_dir, 'cache.db')
            if os.path.exists(cache_file):
                os.remove(cache_file)
                __stitch_plan_cache = diskcache.Cache(stitch_plan_dir, size=size_limit)
        __stitch_plan_cache.size_limit = size_limit

        # reset cache if warnings appear within the files
        warnings = __stitch_plan_cache.check()
        if warnings:
            __stitch_plan_cache.clear()

        atexit.register(__stitch_plan_cache.close)
    return __stitch_plan_cache


def is_cache_disabled():
    return not global_settings['cache_size']


class CacheKeyGenerator(object):
    """Generate cache keys given arbitrary data.

    Given arbitrary data, generate short cache key that is extremely likely
    to be unique.

    Use example:

        >>> generator = CacheKeyGenerator()
        >>> generator.update(b'12345')
        >>> generator.update([1, 2, 3, {4, 5, 6}])
        >>> generator.get_cache_key()
    """

    def __init__(self):
        # SHA1 is chosen for speed.  We don't need cryptography-grade hashing
        # for this use case.
        self._hasher = hashlib.sha1()

    def update(self, data):
        """Provide data to be hashed into a cache key.

        Arguments:
            data -- a bytes object or any object that can be pickled
        """

        if not isinstance(data, bytes):
            data = pickle.dumps(data)

        self._hasher.update(data)

    def get_cache_key(self):
        return self._hasher.hexdigest()
