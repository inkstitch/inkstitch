# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

def get_pagecolor(namedview, default_color='white'):
    pagecolor = default_color
    if namedview is not None:
        pagecolor = namedview.get('pagecolor', pagecolor)
    return pagecolor
