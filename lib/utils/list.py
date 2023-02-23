import random


def _uniform_rng():
    while True:
        yield random.uniform(0, 1)


_rng = _uniform_rng()


def poprandom(sequence, rng=_rng):
    index = int(round(next(rng) * (len(sequence) - 1)))
    item = sequence[index]

    # It's O(1) to pop the last item, and O(n) to pop any other item. So we'll
    # always pop the last item and put it in the slot vacated by the item we're
    # popping.
    last_item = sequence.pop()
    if index < len(sequence):
        sequence[index] = last_item

    return item
