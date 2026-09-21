# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import wx
from typing import Optional

from .animator import Animator
from ...stitch_plan import StitchPlan
from ...i18n import _

# L10N command label at bottom of simulator window
COMMAND_NAMES = [_("STITCH"), _("JUMP"), _("TRIM"), _("STOP"), _("COLOR CHANGE")]

STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
COLOR_CHANGE = 4


class StatusBarUpdater:
    def __init__(self, panel: wx.Panel, animator: Animator) -> None:
        # Set initial values as they may be accessed before a stitch plan is available
        # for example through a focus action on the stitch box
        self.commands = [STITCH]

        self.statusbar: Optional[wx.StatusBar] = None
        tlp = panel.GetTopLevelParent()
        if isinstance(tlp, wx.Frame):  # This should probably always be true, but for type safety's sake...
            self.statusbar = tlp.GetStatusBar()

        animator.add_callback(self._on_current_stitch)

    def set_stitch_plan(self, stitch_plan: Optional[StitchPlan]) -> None:
        if stitch_plan is None:
            if self.statusbar is not None:
                self.statusbar.SetStatusText("", 1)
                self.statusbar.SetStatusText("", 2)
            return

        # Parse commands
        # There is no 0th stitch, so add a place-holder.
        self.commands = [STITCH]

        for color_block in stitch_plan:
            for stitch in color_block:
                if stitch.trim:
                    self.commands.append(TRIM)
                elif stitch.jump:
                    self.commands.append(JUMP)
                elif stitch.stop:
                    self.commands.append(STOP)
                elif stitch.color_change:
                    self.commands.append(COLOR_CHANGE)
                else:
                    self.commands.append(STITCH)

        # Update size element
        if self.statusbar is not None:
            status_text = _("Dimensions: {:.2f} x {:.2f}").format(
                *stitch_plan.dimensions_mm,
            )
            self.statusbar.SetStatusText(status_text, 1)

    def _on_current_stitch(self, current_stitch: int, animating: bool) -> None:
        if self.statusbar is not None:
            try:
                command = self.commands[current_stitch]
            except IndexError:
                # no stitch plan loaded yet, do nothing for now
                return

            self.statusbar.SetStatusText(_("Command: %s") % COMMAND_NAMES[command], 2)
