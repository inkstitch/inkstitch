from hashlib import blake2s
from math import ceil
from itertools import count, chain
import numpy as np


def joinArgs(*args):
    # Stringifies parameters into a slash-separated string for use in hash keys.
    # Idempotent and associative.
    return "/".join([str(x) for x in args])


MAX_UNIFORM_INT = 2 ** 32 - 1


def uniformInts(*args):
    # Single pseudo-random drawing determined by the joined parameters.
    # Returns 4 uniformly random uint64.
    s = joinArgs(*args)
    h = blake2s(s.encode()).hexdigest()
    nums = []
    for i in range(0, 64, 8):
        nums.append(int(h[i:i+8], 16))
    return np.array(nums)


def uniformFloats(*args):
    # returns an array of 8 floats in the range [0,1]
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
