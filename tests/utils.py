from lib.debug.debug import sew_stack_enabled


def element_count():
    element_count = 1
    if sew_stack_enabled:
        element_count = 2
    return element_count
