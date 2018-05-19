try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

# simplify use of lru_cache decorator
def cache(*args, **kwargs):
    return lru_cache(maxsize=None)(*args, **kwargs)
