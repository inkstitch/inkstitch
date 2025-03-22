# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import BaseElement


def prepare_tartan_fill_element(element: BaseElement) -> None:
    """Prepares an svg element to be rendered as a tartan_fill embroidery element

    :param element: svg element with a fill color (path, rectangle, or circle)
    """
    parent_group = element.getparent()
    if parent_group is not None and parent_group.get_id().startswith('inkstitch-tartan'):
        # apply tartan group transform to element
        transform = element.transform @ parent_group.transform
        element.set('transform', transform)
        # remove tartan group and place element in parent group
        outer_group = parent_group.getparent()
        assert outer_group is not None, f"Tartan element {element.get_id()} should have a parent group"
        outer_group.insert(outer_group.index(parent_group), element)
        parent_group.delete()
    # make sure the element is invisible
    element.style['display'] = 'inline'
