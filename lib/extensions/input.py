# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from lxml import etree

from ..stitch_plan import generate_stitch_plan


class Input(object):
    def run(self, args):
        embroidery_file = args[0]
        stitch_plan = generate_stitch_plan(embroidery_file)
        print(etree.tostring(stitch_plan).decode('utf-8'))
