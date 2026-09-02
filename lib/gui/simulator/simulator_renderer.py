# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
from threading import Event, Thread

import wx

from ...debug.debug import debug
from ...utils.threading import ExitThread
from ...stitch_plan import StitchPlan
from typing import Callable, Optional

RenderFunction = Callable[[], Optional[StitchPlan]]

class PreviewRenderer(Thread):
    """Render stitch plan in a background thread."""

    def __init__(
            self,
            render_stitch_plan: RenderFunction,
            rendering_completed: Callable[[StitchPlan | None], None]
            ) -> None:
        super(PreviewRenderer, self).__init__()
        self.daemon = True
        self.refresh_needed = Event()

        self.render_stitch_plan = render_stitch_plan
        self.rendering_completed = rendering_completed

        # This is read by utils.threading.check_stop_flag() to abort stitch plan
        # generation.
        self.stop = Event()

    def update(self) -> None:
        """Request to render a new stitch plan.

        self.render_stitch_plan() will be called in a background thread, and then
        self.rendering_completed() will be called with the resulting stitch plan.
        """

        if not self.is_alive():
            self.start()

        self.stop.set()
        self.refresh_needed.set()

    def run(self) -> None:
        while True:
            self.refresh_needed.wait()
            self.refresh_needed.clear()
            self.stop.clear()

            try:
                debug.log("update_patches")

                stitch_plan = self.render_stitch_plan()
                # rendering_completed() will be called in the main thread.
                wx.CallAfter(self.rendering_completed, stitch_plan)

            except ExitThread:
                debug.log("ExitThread caught")
            except:  # noqa: E722
                import traceback
                debug.log("unhandled exception in PreviewRenderer.render_stitch_plan(): " + traceback.format_exc())
