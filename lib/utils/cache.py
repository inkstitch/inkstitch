# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import os
import atexit
import hashlib
import pickle

import appdirs
import diskcache

from lib.utils.settings import global_settings

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


# simplify use of lru_cache decorator
def cache(*args, **kwargs):
    return lru_cache(maxsize=None)(*args, **kwargs)


__stitch_plan_cache = None


def get_stitch_plan_cache():
    global __stitch_plan_cache

    if __stitch_plan_cache is None:
        cache_dir = os.path.join(appdirs.user_config_dir('inkstitch'), 'cache', 'stitch_plan')
        size_limit = global_settings['cache_size'] * 1024 * 1024
        __stitch_plan_cache = diskcache.Cache(cache_dir, size=size_limit)
        __stitch_plan_cache.size_limit = size_limit
        atexit.register(__stitch_plan_cache.close)

    return __stitch_plan_cache


def is_cache_disabled():
    return global_settings['disable_cache']


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
