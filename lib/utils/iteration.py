def flatten(thing):
    """Iterate through all nested iterables in the argument."""

    try:
        iterable = iter(iterable)
    except TypeError:
        yield thing

    for item in thing:
        for sub_item in flatten(item):
            yield sub_item
