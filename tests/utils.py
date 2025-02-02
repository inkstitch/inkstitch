from lib.debug.utils import safe_get
from lib.utils.paths import get_ini


def element_count():
    element_count = 1
    if safe_get(get_ini(), "DEBUG", "sew_stack_enable", default=False):
        element_count = 2
    return element_count
