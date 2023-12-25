# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.


def prepare_tartan_fill_element(element):
    parent_group = element.getparent()
    if parent_group.get_id().startswith('inkstitch-tartan'):
        # apply tartan group transform to element
        transform = element.transform @ parent_group.transform
        element.set('transform', transform)
        # remove tartan group and place element in parent group
        outer_group = parent_group.getparent()
        outer_group.insert(outer_group.index(parent_group), element)
        outer_group.remove(parent_group)
    # make sure the element is invisible
    element.style['display'] = 'inline'
