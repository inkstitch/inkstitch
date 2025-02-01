from lib.debug.utils import get_ini, safe_get


def element_count():
    element_count = 1
    if safe_get(get_ini(), "DEBUG", "sew_stack_enable", default=False):
        element_count = 2
    import sys
    print(element_count)
    return element_count
