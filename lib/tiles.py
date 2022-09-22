import inkex
from math import ceil, floor
from networkx import Graph
import os
from shapely.geometry import LineString
from shapely.prepared import prep

from .svg import apply_transforms
from .utils import get_bundled_dir, guess_inkscape_config_path, Point
from random import random


class Tile:
    def __init__(self, path):
        self._load_tile(path)

    def _load_tile(self, tile_path):
        tile_svg = inkex.load_svg(tile_path)
        self.name = self._get_name(tile_path)
        self._load_paths(tile_svg)
        self._load_dimensions(tile_svg)
        self._load_buffer_size(tile_svg)
        self._load_parallelogram(tile_svg)

    def __repr__(self):
        return f"Tile({self.name}, {self.shift0}, {self.shift1})"

    __str__ = __repr__

    def _get_name(self, tile_path):
        return os.path.splitext(os.path.basename(tile_path))[0]

    def _load_paths(self, tile_svg):
        path_elements = tile_svg.findall('.//svg:path', namespaces=inkex.NSS)
        self.tile = self._path_elements_to_line_strings(path_elements)
        # self.center, ignore, ignore = self._get_center_and_dimensions(self.tile)

    def _load_dimensions(self, tile_svg):
        svg_element = tile_svg.getroot()
        self.width = svg_element.viewport_width
        self.height = svg_element.viewport_height

    def _load_buffer_size(self, tile_svg):
        circle_elements = tile_svg.findall('.//svg:circle', namespaces=inkex.NSS)
        if circle_elements:
            self.buffer_size = circle_elements[0].radius
        else:
            self.buffer_size = 0

    def _load_parallelogram(self, tile_svg):
        parallelogram_elements = tile_svg.findall(".//svg:*[@class='para']", namespaces=inkex.NSS)
        if parallelogram_elements:
            path_element = parallelogram_elements[0]
            path = apply_transforms(path_element.get_path(), path_element)
            subpaths = path.to_superpath()
            subpath = subpaths[0]
            points = [Point.from_tuple(p[1]) for p in subpath]
            self.shift0 = points[1] - points[0]
            self.shift1 = points[2] - points[1]
        else:
            self.shift0 = Point(self.width, 0)
            self.shift1 = Point(0, self.height)

    def _path_elements_to_line_strings(self, path_elements):
        lines = []
        for path_element in path_elements:
            path = apply_transforms(path_element.get_path(), path_element)
            for subpath in path.to_superpath():
                # We only care about the endpoints of each subpath.  They're
                # supposed to be simple line segments.
                lines.append([Point.from_tuple(subpath[0][1]), Point.from_tuple(subpath[-1][1])])

        return lines

    def _get_center_and_dimensions(self, shape):
        min_x, min_y, max_x, max_y = shape.bounds
        center = Point((max_x + min_x) / 2, (max_y + min_y) / 2)
        width = max_x - min_x
        height = max_y - min_y

        return center, width, height

    def translate_tile(self, shift):
        translated_tile = []

        for start, end in self.tile:
            start += shift
            end += shift
            translated_tile.append((start.as_int().as_tuple(), end.as_int().as_tuple()))

        return translated_tile

    def to_graph(self, shape, only_inside=True, pad=True):
        """Apply this tile to a shape, repeating as necessary.

        Return value:
            networkx.Graph with edges corresponding to lines in the pattern.
              Each edge has an attribute 'line_string' with the LineString
              representation of this edge.
        """
        shape_center, shape_width, shape_height = self._get_center_and_dimensions(shape)
        shape_diagonal = (shape_width ** 2 + shape_height ** 2) ** 0.5
        graph = Graph()

        if pad:
            shape = shape.buffer(-self.buffer_size)

        prepared_shape = prep(shape)

        tiles0 = ceil(shape_diagonal / self.shift0.length()) + 2
        tiles1 = ceil(shape_diagonal / self.shift1.length()) + 2
        for repeat0 in range(floor(-tiles0 / 2), ceil(tiles0 / 2)):
            for repeat1 in range(floor(-tiles1 / 2), ceil(tiles1 / 2)):
                shift0 = repeat0 * self.shift0 + shape_center
                shift1 = repeat1 * self.shift1 + shape_center
                this_tile = self.translate_tile(shift0 + shift1)
                for line in this_tile:
                    line_string = LineString(line)
                    if not only_inside or prepared_shape.contains(line_string):
                        graph.add_edge(line[0], line[1], line_string=line_string, weight=random() + 0.1)

        return graph


def all_tile_paths():
    return [os.path.join(guess_inkscape_config_path(), 'tiles'),
            get_bundled_dir('tiles')]


def all_tiles():
    for tile_dir in all_tile_paths():
        try:
            for tile_file in sorted(os.listdir(tile_dir)):
                yield Tile(os.path.join(tile_dir, tile_file))
        except FileNotFoundError:
            pass
