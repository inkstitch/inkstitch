from lib.debug.debug import sew_stack_enabled

# Mark this module as non-test, otherwise pytest thinks the contents of this file are tests,
# despite element_count obviously not having "test" in its name???
__test__ = False

def element_count() -> int:
    element_count = 1
    if sew_stack_enabled:
        element_count = 2
    return element_count
