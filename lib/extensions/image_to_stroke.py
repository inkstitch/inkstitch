# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import base64
import os
from io import BytesIO

import inkex
import networkx as nx
from PIL import Image, ImageFilter, ImageOps
from scipy.spatial import Delaunay

from ..i18n import _
from ..stitches.meander_fill import generate_meander_path
from ..svg import PIXELS_PER_MM
from ..svg.tags import XLINK_HREF
from ..utils.prng import iter_uniform_floats
from .base import InkstitchExtension


class ImageToStroke(InkstitchExtension):
    def effect(self):
        images = [image for image in self.svg.selection if image.TAG == "image"]
        if not images:
            inkex.errormsg(_("Please select at least one image."))
            return

        for i, image in enumerate(images):
            width = int(float(image.get('width', '64')))
            height = int(float(image.get('height', '64')))
            parent = image.getparent()
            index = parent.index(image) + 1

            image_byte_string = self._get_image_byte_string(image)
            if not image_byte_string:
                continue
            with Image.open(image_byte_string) as img:
                image_data = img.resize((width, height)).convert('L')
                image_data = ImageOps.autocontrast(image_data, 10)

            graph = self._get_delauney_graph(image_data)
            rng = iter_uniform_floats(image.get_id() or '', 'embroider-image', i)
            width, height = image_data.size
            start = list(graph.nodes)[0]
            end = list(graph.nodes)[-1]
            points = generate_meander_path(graph, start, end, rng)

            d = "M" + " ".join(" ".join(str(coord) for coord in point) for point in points)
            style = 'fill:none;stroke-width:0.264;stroke:black;stroke-dasharray:3, 1;'
            parent.insert(index, inkex.PathElement(d=d, style=style))

    def _get_delauney_graph(self, image):
        dotlist = []
        pixels = image.load()
        width, height = image.size
        contrasts = [(0, 64), (64, 127), (128, 160), (161, 190)]
        # we do not need to set points which are too close to each other (minimum: 1 mm)
        # so let's skip some pixels
        for i, contrast in enumerate(contrasts):
            for y in range(0, height - 1, int(PIXELS_PER_MM)):
                for x in range(0, width - 1, int(PIXELS_PER_MM)):
                    j = i * 2 if i > 0 else 1
                    if y % j != 0 or x % j != 0:
                        continue
                    if pixels[x, y] in range(contrast[0], contrast[1]):
                        dotlist.append((x, y))

        # add some extra points at edges (needed?)
        image = image.filter(ImageFilter.FIND_EDGES)
        image = ImageOps.invert(image)
        pixels = image.load()
        for y in range(0, height - 1, int(PIXELS_PER_MM / 1.5)):
            for x in range(0, width - 1, int(PIXELS_PER_MM / 1.5)):
                if pixels[x, y] in range(0, 50) and x not in (0, width) and y not in (0, height):
                    dotlist.append((x, y))

        graph = nx.Graph()
        tri = Delaunay(dotlist)
        graph.add_nodes_from(dotlist)

        # create a list of edges which are all connected to one other edge
        for indexes in tri.simplices:
            graph.add_edge(dotlist[indexes[0]], dotlist[indexes[1]])
            graph.add_edge(dotlist[indexes[1]], dotlist[indexes[2]])
            graph.add_edge(dotlist[indexes[2]], dotlist[indexes[0]])

        return graph

    def _get_image_byte_string(self, image):
        if isinstance(image, inkex.Image):
            image = image.get(XLINK_HREF, None)
            if not image:
                return
            # linked image
            if image.startswith('file'):
                image_string = image[7:]
                if not os.path.isfile(image_string):
                    return
            # embedded imagae
            elif image.startswith('data'):
                image = image.split(',', 1)
                image_string = BytesIO(base64.b64decode(image[1]))
        return image_string
