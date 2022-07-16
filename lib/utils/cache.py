# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import os
import atexit

import appdirs
import diskcache

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
        __stitch_plan_cache = diskcache.Cache(cache_dir, size=1024 * 1024 * 100)
        atexit.register(__stitch_plan_cache.close)

    return __stitch_plan_cache
