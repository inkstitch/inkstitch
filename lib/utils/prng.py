from hashlib import blake2s
from math import ceil
from itertools import count, chain
import numpy as np

# Framework for reproducable pseudo-random number generation.

# Unlike python's random module (which uses a stateful generator based on global variables),
# a counter-mode PRNG like uniformFloats can be used to generate multiple, independent random streams
# by including an additional parameter before the loop counter.
# This allows different aspects of an embroidery element to not effect each other's rolls,
# making random generation resistant to small edits in the control paths or refactoring.
# Using multiple counters for n-dimentional random streams is also possible and is useful for grid-like structures.


def joinArgs(*args):
    # Stringifies parameters into a slash-separated string for use in hash keys.
    # Idempotent and associative.
    return "/".join([str(x) for x in args])


MAX_UNIFORM_INT = 2 ** 32 - 1


def uniformInts(*args):
    # Single pseudo-random drawing determined by the joined parameters.
    # To get a longer sequence of random numbers, call this loop with a counter as one of the parameters.
    # Returns 8 uniformly random uint32.

    s = joinArgs(*args)
    # blake2s is python's fastest hash algorithm for small inputs and is designed to be usable as a PRNG.
    h = blake2s(s.encode()).hexdigest()
    nums = []
    for i in range(0, 64, 8):
        nums.append(int(h[i:i+8], 16))
    return np.array(nums)


def uniformFloats(*args):
    # Single pseudo-random drawing determined by the joined parameters.
    # To get a longer sequence of random numbers, call this loop with a counter as one of the parameters.
    # Returns an array of 8 floats in the range [0,1]
    return uniformInts(*args) / MAX_UNIFORM_INT


def nUniformFloats(n: int, *args):
    # returns a fixed number (which may exceed 8) of floats in the range [0,1]
    seed = joinArgs(*args)
    nBlocks = ceil(n/8)
    blocks = [uniformFloats(seed, x) for x in range(nBlocks)]
    return np.concatenate(blocks)[0:n]


def iterUniformFloats(*args):
    # returns an infinite sequence of floats in the range [0,1]
    seed = joinArgs(*args)
    blocks = map(lambda x: list(uniformFloats(seed, x)), count(0))
    return chain.from_iterable(blocks)
