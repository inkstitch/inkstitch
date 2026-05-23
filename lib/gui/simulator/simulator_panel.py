# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import wx
import time

from . import ControlPanel, DrawingPanel, ViewPanel
from ...stitch_plan import StitchPlan
from typing import List, Optional, cast
from ...utils.settings import global_settings
from ...i18n import _

# L10N command label at bottom of simulator window
COMMAND_NAMES = [_("STITCH"), _("JUMP"), _("TRIM"), _("STOP"), _("COLOR CHANGE")]

# Constants corresponding to indices in the above array
STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
COLOR_CHANGE = 4


class SimulatorPanel(wx.Panel):
    """
    Panel for the Simulator, with a drawing panel, control panel, and view panel.

    Owns animation control.
    """

    # render no faster than this many frames per second
    TARGET_FPS = 30
    TARGET_FRAME_PERIOD = 1.0 / TARGET_FPS

    def __init__(self, parent, stitch_plan=None, background_color='white', target_duration=5, stitches_per_second=16, detach_callback=None) -> None:
        """"""
        super().__init__(parent, style=wx.BORDER_SUNKEN)

        self.animating = False
        self.timer = wx.Timer(self)
        self.last_frame_start = 0.0
        self.direction: float = 1
        self.current_stitch: int = 0
        # Set initial values as they may be accessed before a stitch plan is available
        # for example through a focus action on the stitch box
        self.num_stitches = 1
        self.commands: List[int] = []

        # desired simulation speed in stitches per second
        self.speed: int = global_settings['simulator_speed']

        self.Bind(wx.EVT_TIMER, self.animate)

        self.cp = ControlPanel(
            self,
            stitch_plan=stitch_plan,
            stitches_per_second=stitches_per_second,
            target_duration=target_duration,
            detach_callback=detach_callback
        )

        self.vp = ViewPanel(
            self,
            detach_callback,
            stitch_plan=stitch_plan,
        )
        self.dp = DrawingPanel(self)
        self.vp.set_drawing_panel(self.dp)
        self.vp.set_background_color(wx.Colour(background_color))
        self.dp.set_background_color(wx.Colour(background_color))

        dvSizer = wx.BoxSizer(wx.HORIZONTAL)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.dp, 1, wx.EXPAND | wx.ALL, 2)
        vbSizer.Add(self.cp, 0, wx.EXPAND | wx.ALL, 2)

        dvSizer.Add(vbSizer, 1, wx.EXPAND | wx.ALL, 2)
        dvSizer.Add(self.vp, 0, wx.ALL, 2)

        self.SetSizerAndFit(dvSizer)

        # Keyboard Shortcuts
        shortcut_keys = [
            (wx.ACCEL_NORMAL, wx.WXK_RIGHT, self.cp.animation_forward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_RIGHT, self.cp.animation_forward),
            (wx.ACCEL_NORMAL, wx.WXK_LEFT, self.cp.animation_reverse),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_LEFT, self.cp.animation_reverse),
            (wx.ACCEL_NORMAL, wx.WXK_UP, self.cp.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_UP, self.cp.animation_speed_up),
            (wx.ACCEL_NORMAL, wx.WXK_DOWN, self.cp.animation_slow_down),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_DOWN, self.cp.animation_slow_down),
            (wx.ACCEL_NORMAL, ord('+'), self.cp.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, ord('='), self.cp.animation_one_stitch_forward),
            (wx.ACCEL_SHIFT, ord('='), self.cp.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, wx.WXK_ADD, self.cp.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_ADD, self.cp.animation_one_stitch_forward),
            (wx.ACCEL_NORMAL, ord('-'), self.cp.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, ord('_'), self.cp.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, wx.WXK_SUBTRACT, self.cp.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_SUBTRACT, self.cp.animation_one_stitch_backward),
            (wx.ACCEL_NORMAL, ord('r'), self.restart),
            (wx.ACCEL_NORMAL, ord('p'), self.cp.play_or_pause),
            (wx.ACCEL_NORMAL, wx.WXK_SPACE, self.cp.play_or_pause),
            (wx.ACCEL_NORMAL, wx.WXK_PAGEDOWN, self.cp.animation_one_command_backward),
            (wx.ACCEL_NORMAL, wx.WXK_PAGEUP, self.cp.animation_one_command_forward),
            (wx.ACCEL_NORMAL, ord('o'), self.vp.on_toggle_npp_shortcut)
        ]

        self.accel_entries = []

        for shortcut_key in shortcut_keys:
            eventId = wx.NewIdRef()
            self.accel_entries.append((shortcut_key[0], shortcut_key[1], eventId))
            self.Bind(wx.EVT_MENU, shortcut_key[2], id=eventId)

        self.accel_table = wx.AcceleratorTable(self.accel_entries)
        self.SetAcceleratorTable(self.accel_table)

        # wait for layouts so that panel size is set
        if stitch_plan:
            wx.CallLater(50, self.dp.load, stitch_plan)

    def load(self, stitch_plan: StitchPlan) -> None:
        self.num_stitches = stitch_plan.num_stitches
        self.dp.load(stitch_plan)
        self.cp.load(stitch_plan)
        self.vp.load(stitch_plan)

        # Build command list used to fill out the statusbar
        # There is no 0th stitch, so add a place-holder.
        self.commands = []
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

        statusbar = cast(wx.Frame, self.GetTopLevelParent()).GetStatusBar()
        statusbar.SetStatusText(
            _("Dimensions: {:.2f} x {:.2f}").format(
                stitch_plan.dimensions_mm[0],
                stitch_plan.dimensions_mm[1]
            ),
            1
        )

        self.go()

    def clear(self) -> None:
        self.dp.clear()
        self.cp.clear()
        self.vp.load(None)

    def set_page_specs(self, page_specs: dict) -> None:
        self.dp.set_page_specs(page_specs)

    # Animation/Current Stitch-related methods
    # Could probably be refactored into an "AnimationController" class in the future
    # to better decouple the simulator elements from their panel...

    def go(self) -> None:
        if not self.animating:
            try:
                self.animating = True
                self.last_frame_start = 0
                self.timer.Start(int(self.TARGET_FRAME_PERIOD * 1000))
                self.animate()
                self.cp.on_start()
            except RuntimeError:
                pass

    def stop(self) -> None:
        self.animating = False
        self.timer.Stop()
        self.cp.on_stop()

    def forward(self) -> None:
        self.direction = 1
        self.start_if_not_at_end()

    def reverse(self) -> None:
        self.direction = -1
        self.start_if_not_at_end()

    def restart(self, event: Optional[wx.Event] = None) -> None:
        if self.direction == 1:
            self.current_stitch = 1
        elif self.direction == -1:
            self.current_stitch = self.num_stitches

        self.go()

    def one_stitch_forward(self) -> None:
        self.set_current_stitch(self.current_stitch + 1)

    def one_stitch_backward(self) -> None:
        self.set_current_stitch(self.current_stitch - 1)

    def stop_if_at_end(self) -> None:
        if self.direction == -1 and self.current_stitch == 1:
            self.stop()
        elif self.direction == 1 and self.current_stitch == self.num_stitches:
            self.stop()

    def start_if_not_at_end(self) -> None:
        if self.direction == -1 and self.current_stitch > 1:
            self.go()
        elif self.direction == 1 and self.current_stitch < self.num_stitches:
            self.go()

    def animate(self, event: Optional[wx.Event] = None) -> None:
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
            frame_time = self.TARGET_FRAME_PERIOD
        self.last_frame_start = now

        stitch_increment = self.speed * frame_time
        self.set_current_stitch(int(self.current_stitch + self.direction * stitch_increment))

        self.stop_if_at_end()

    def set_current_stitch(self, current_stitch: int) -> None:
        # Clamp current stitch value
        if current_stitch < 1:
            current_stitch = 1
        elif current_stitch > self.num_stitches:
            current_stitch = self.num_stitches

        self.current_stitch = current_stitch

        self.dp.set_current_stitch(self.current_stitch)
        self.cp.on_current_stitch(self.current_stitch)

        # Todo: Should this maybe be in that top-level parent?
        try:
            command = self.commands[self.current_stitch-1]
            statusbar = cast(wx.Frame, self.GetTopLevelParent()).GetStatusBar()
            statusbar.SetStatusText(_("Command: %s") % COMMAND_NAMES[command], 2)
        except IndexError:
            # no stitch plan loaded yet, do nothing for now
            pass

    def set_speed(self, speed: int) -> None:
        self.speed = speed
        global_settings['simulator_speed'] = speed
