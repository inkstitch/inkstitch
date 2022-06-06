# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from lxml import etree
from inkex import errormsg
from ..i18n import _
from ..stitch_plan import generate_stitch_plan


class Input(object):
    def run(self, args):
        embroidery_file = args[0]
        if args[0].endswith(('edr', 'col', 'inf')):
            msg = _("Ink/Stitch cannot import color formats directly. But you can open the embroidery file and apply the color with "
                    "Extensions > Ink/Stitch > Thread Color Management > Apply Threadlist")
            errormsg(msg)
            exit(0)
        stitch_plan = generate_stitch_plan(embroidery_file)
        print(etree.tostring(stitch_plan).decode('utf-8'))
