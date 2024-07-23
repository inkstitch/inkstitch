# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import base64
import os
from io import BytesIO

import inkex
from PIL import Image, ImageOps

from ..i18n import _
from ..svg.tags import XLINK_HREF
from .base import InkstitchExtension


class Stereogram(InkstitchExtension):
    def effect(self):
        images = [image for image in self.svg.selection if image.TAG == "image"]
        groups = [group for group in self.svg.selection if group.TAG == "g"]
        if not images or not groups:
            inkex.errormsg(_("Please select one image and one group."))
            return

        # select first image only
        image = images[0]
        image_bbox = image.bounding_box()
        width = self.to_pixel_integer(image_bbox.width)
        height = self.to_pixel_integer(image_bbox.height)

        image_byte_string = self._get_image_byte_string(image)
        if not image_byte_string:
            inkex.errormsg(_("Couldn't read the selected image."))
            return
        with Image.open(image_byte_string) as img:
            image_data = img.resize((width, height)).convert('L')
            image_data = ImageOps.autocontrast(image_data, (0, 0))
        self.pixels = image_data.load()

        # move group to the left of the canvas
        group = groups[0]
        group_bbox = group.bounding_box()
        transform_x = -group_bbox.right
        transform_y = -(group_bbox.height - image_bbox.height) / 2 - group_bbox.top
        group_transform = group.composed_transform() @ inkex.Transform(translate=(transform_x, transform_y))
        group_width = group_bbox.width

        # select first group only
        for path in group.iterchildren():
            path.transform @= group_transform
            for i in range(int(width / self.to_pixel_integer(group_width)) + 1):
                path = self.shift_and_transform(path, group_width, image_bbox.width)

    def shift_and_transform(self, path, group_width, image_width):
        path = path.duplicate()
        path.transform @= inkex.Transform(translate=(group_width, 0))
        path.apply_transform()
        points = path.get_path().end_points
        new_points = []
        last_point_outside = 0
        for point in points:
            try:
                move = self.pixels[
                    max(0, self.to_pixel_integer(point.x)),
                    max(0, self.to_pixel_integer(point.y))
                ]
                new_points.append((point.x-move/150, point.y-move/150))
                last_point_outside = 0
            except IndexError:
                if point.x > image_width:
                    point.x = image_width
                    last_point_outside += 1
                if last_point_outside <= 1:
                    new_points.append((point.x, point.y))
        path.set('d', str(inkex.Path(new_points)))
        return path

    def to_pixel_integer(self, value):
        value = f"{value}{self.svg.unit}"
        return int(inkex.units.convert_unit(value, 'px'))

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
