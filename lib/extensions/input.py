# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from html import unescape
from sys import exit, platform

from inkex import errormsg
from lxml import etree

from ..i18n import _
from ..metadata import InkStitchMetadata
from ..stitch_plan import generate_stitch_plan
from ..update import INKSTITCH_SVG_VERSION


class Input(object):
    def run(self, args):
        embroidery_file = args[0]
        if args[0].endswith(('edr', 'col', 'inf')):
            msg = _("Ink/Stitch cannot import color formats directly. But you can open the embroidery file and apply the color with "
                    "Extensions > Ink/Stitch > Thread Color Management > Apply Threadlist")
            errormsg(msg)
            exit(0)
        stitch_plan = generate_stitch_plan(embroidery_file)

        # Set SVG Version so we do request the user to update the document later on
        metadata = InkStitchMetadata(stitch_plan)
        metadata['inkstitch_svg_version'] = INKSTITCH_SVG_VERSION

        out = etree.tostring(stitch_plan).decode('utf-8')
        if platform == "win32":
            print(out)
        else:
            print(unescape(out))
