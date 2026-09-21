# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import wx
import time

from typing import Callable, Optional, Set
from ...stitch_plan import StitchPlan
from ...utils.settings import global_settings

AnimatorCallback = Callable[[int, bool], None]


class Animator:
    """ Time control for the simulator """

    # render no faster than this many frames per second
    TARGET_FPS = 30

    def __init__(self, stitch_plan: Optional[StitchPlan]) -> None:
        self.animating = False

        self.callbacks: Set[AnimatorCallback] = set()

        # This is a float because we accumulate "fractional" stitches, particularly in cases when the stitch rate
        # is less than the frame rate. This is converted to int before being sent to callbacks.
        self.current_stitch: float = 1.0
        self.direction = 1
        self.target_frame_period = 1.0 / self.TARGET_FPS
        self.last_frame_start = 0.0

        # desired simulation speed in stitches per second
        self.speed: int = global_settings['simulator_speed']

        self.timer = wx.Timer()
        self.timer.Bind(wx.EVT_TIMER, self._animate)

        self.set_stitch_plan(stitch_plan)

    def set_stitch_plan(self, stitch_plan: Optional[StitchPlan]):
        self.stitch_plan = stitch_plan
        self.current_stitch = 1.0
        self.direction = 1

        if stitch_plan is not None:
            self.go()
        else:
            self.stop()

    def add_callback(self, callback: AnimatorCallback) -> None:
        self.callbacks.add(callback)
        callback(int(self.current_stitch), self.animating)

    def remove_callback(self, callback: AnimatorCallback) -> None:
        self.callbacks.remove(callback)

    def _clamp_current_stitch(self) -> None:
        if self.stitch_plan is None:
            return

        if self.current_stitch < 1:
            self.current_stitch = 1
        elif self.current_stitch > self.stitch_plan.num_stitches:
            self.current_stitch = self.stitch_plan.num_stitches

    def _stop_if_at_end(self) -> None:
        if self.stitch_plan is None:
            return

        if self.direction == -1 and self.current_stitch == 1:
            self.stop()
        elif self.direction == 1 and self.current_stitch == self.stitch_plan.num_stitches:
            self.stop()

    def _start_if_not_at_end(self) -> None:
        if self.stitch_plan is None:
            return

        if self.direction == -1 and self.current_stitch > 1:
            self.go()
        elif self.direction == 1 and self.current_stitch < self.stitch_plan.num_stitches:
            self.go()

    def _animate(self, event: Optional[wx.TimerEvent] = None) -> None:
        if not self.animating:
            return

        # Each frame, we need to advance forward some number of stitches to
        # match the speed setting.  The tricky thing is that with bigger
        # designs, it may take a long time to render a frame.  That might
        # mean that we'll fall behind.  Even if we set our Timer to 30 FPS,
        # we may only actually manage to render 20 FPS or fewer, and the
        # duration of each frame may vary.
        #
        # To deal with that, we'll figure out how many stitches to advance
        # based on how long it took to render the last frame.  We'll always
        # be behind by one frame, but it should work out fine.

        now = time.time()
        if self.last_frame_start:
            frame_time = now - self.last_frame_start
        else:
            frame_time = self.target_frame_period
        self.last_frame_start = now

        stitch_increment = self.speed * frame_time
        self.set_current_stitch(self.current_stitch + self.direction * stitch_increment)

    def stop(self) -> None:
        self.animating = False
        self.timer.Stop()

    def go(self) -> None:
        if self.stitch_plan is None:
            return

        if not self.animating:
            try:
                self.animating = True
                self.last_frame_start = 0
                self.timer.Start(int(self.target_frame_period * 1000))
                self._animate()
            except RuntimeError:
                pass

    def forward(self) -> None:
        self.direction = 1
        self._start_if_not_at_end()

    def reverse(self) -> None:
        self.direction = -1
        self._start_if_not_at_end()

    def set_current_stitch(self, stitch: float) -> None:
        self.current_stitch = stitch
        self._clamp_current_stitch()
        self._stop_if_at_end()
        for callback in self.callbacks:
            callback(int(self.current_stitch), self.animating)

    def restart(self) -> None:
        if self.stitch_plan is None:
            return

        if self.direction == 1:
            self.current_stitch = 1
        elif self.direction == -1:
            self.current_stitch = self.stitch_plan.num_stitches

        self.go()

    def one_stitch_forward(self) -> None:
        self.set_current_stitch(self.current_stitch + 1)

    def one_stitch_backward(self) -> None:
        self.set_current_stitch(self.current_stitch - 1)

    def show_all_stitches(self, event: wx.CommandEvent) -> None:
        if self.stitch_plan is None:
            return

        self.stop()
        self.set_current_stitch(self.stitch_plan.num_stitches)

    def set_speed(self, speed: int) -> None:
        self.speed = speed
        global_settings['simulator_speed'] = speed
