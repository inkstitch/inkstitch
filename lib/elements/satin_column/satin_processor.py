import numpy as np

from .satin_column import SatinColumn
from ...utils import prng, Point, offset_points


class SatinProcessor:
    def __init__(self, satin: 'SatinColumn', offset_px: tuple[float, float], offset_proportional: tuple[float, float], use_random: bool):
        self.satin = satin
        self.use_random = use_random
        self.offset_px = offset_px
        self.offset_proportional = offset_proportional
        self.random_zigzag_spacing = satin.random_zigzag_spacing

        if use_random:
            self.seed = prng.join_args(satin.random_seed, "satin-points")
            self.offset_proportional_min = np.array(offset_proportional) - satin.random_width_decrease
            self.offset_range = (satin.random_width_increase + satin.random_width_decrease)
            self.cycle = 0

    def process_points(self, pos0: Point, pos1: Point) -> tuple[Point, Point]:
        if self.use_random:
            roll = prng.uniform_floats(self.seed, self.cycle)
            self.cycle += 1
            offset_prop = self.offset_proportional_min + roll[0:2] * self.offset_range
        else:
            offset_prop = self.offset_proportional

        a, b = offset_points(pos0, pos1, self.offset_px, offset_prop)
        return a, b

    def get_stitch_spacing_multiple(self):
        if self.use_random:
            roll = prng.uniform_floats(self.seed, self.cycle)
            self.cycle += 1
            return max(1.0 + ((roll[0] - 0.5) * 2) * self.random_zigzag_spacing, 0.01)
        else:
            return 1.0
