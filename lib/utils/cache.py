# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache  # type: ignore[no-redef]

# simplify use of lru_cache decorator


def cache(*args, **kwargs):
    return lru_cache(maxsize=None)(*args, **kwargs)
