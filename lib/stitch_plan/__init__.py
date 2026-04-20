# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .color_block import ColorBlock as ColorBlock
from .stitch import Stitch as Stitch
from .stitch_group import StitchGroup as StitchGroup
from .stitch_plan import StitchPlan as StitchPlan, stitch_groups_to_stitch_plan as stitch_groups_to_stitch_plan


def __getattr__(name):
    if name == 'generate_stitch_plan':
        from .generate_stitch_plan import generate_stitch_plan
        globals()['generate_stitch_plan'] = generate_stitch_plan
        return generate_stitch_plan
    if name == 'stitch_plan_from_file':
        from .read_file import stitch_plan_from_file
        globals()['stitch_plan_from_file'] = stitch_plan_from_file
        return stitch_plan_from_file
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
