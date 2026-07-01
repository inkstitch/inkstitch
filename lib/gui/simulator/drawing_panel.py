# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import time
from typing import Protocol, Tuple, Optional, List, Dict, Any, cast

import wx

from ...i18n import _
from ...utils.settings import global_settings
from ...stitch_plan import StitchPlan

from .drawing_panel_simple import SimpleDrawingPanel


# L10N command label at bottom of simulator window
COMMAND_NAMES = [_("STITCH"), _("JUMP"), _("TRIM"), _("STOP"), _("COLOR CHANGE")]

STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
COLOR_CHANGE = 4


class DrawingPanelParameterHolder(Protocol):
    # A drawing panel will be passed an instance of DrawingPanelParameterHolder
    # that it can use to look up the current render settings.
    # It should use this as the source of truth and only save values for e.g. caching reasons.

    @property
    def current_stitch() -> int: ...

    # Camera settings
    zoom: float
    pan: Tuple[float, float]

    # Page/Background settings
    page_specs: dict
    background_color: Optional[wx.Colour]

    # Render options
    show_page: bool

    @property
    def draw_cursor(self) -> bool: ...

    @property
    def render_jumps(self) -> bool: ...

    @property
    def render_needle_pen_points(self) -> bool: ...


class DrawingPanelProto(Protocol):
    # Any drawing panel must implement these methods
    def set_stitch_plan(self, stitch_plan: StitchPlan) -> None: ...


class DrawingPanel(wx.Panel):
    """
    Essentially, a holder for an element that does the actual rendering,
    that maintains the renderer state. This way we can switch renderers on
    the fly and keep the same settings.

    This state information probably does not belong in a UI element quite like this, but
    that's a bigger refactor for a later day.
    """

    # render no faster than this many frames per second
    TARGET_FPS = 30

    def __init__(self, parent, *args, **kwargs) -> None:
        """"""
        self.parent = parent
        self.stitch_plan: Optional[StitchPlan] = kwargs.pop('stitch_plan', None)
        kwargs['style'] = wx.BORDER_SUNKEN

        wx.Panel.__init__(self, parent, *args, **kwargs)

        # Drawing panel can really be any size, but without this wxpython likes
        # to allow the status bar and control panel to get squished.
        self.SetMinSize((300, 300))

        self.control_panel = parent.cp
        self.view_panel = parent.vp

        self.renderer: Optional[SimpleDrawingPanel] = None

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.Layout()

        self.animating = False
        self.timer = wx.Timer(self)
        self.last_frame_start = 0.0
        self.target_frame_period = 1.0 / self.TARGET_FPS
        self.direction = 1
        self._current_stitch: float = 0  # Ideally this would be an int, but the animation code as it is now expects this to be a float
        self.width = 0
        self.height = 0
        self.loaded = False
        self.page_specs: Dict[str, Any] = {}
        self.show_page = global_settings['toggle_page_button_status']
        self.background_color: Optional[wx.Colour] = None

        # Set initial values as they may be accessed before a stitch plan is available
        # for example through a focus action on the stitch box
        self.num_stitches = 1
        self.commands: List[int] = [STITCH]

        # desired simulation speed in stitches per second
        self.speed = global_settings['simulator_speed']

        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_TIMER, self.animate)

        # wait for layouts so that panel size is set
        if self.stitch_plan:
            wx.CallLater(50, self.load, self.stitch_plan)

    def on_resize(self, event: wx.SizeEvent) -> None:
        self.choose_zoom_and_pan()
        self.Layout()
        self.Refresh()

    def clamp_current_stitch(self) -> None:
        if self._current_stitch < 1:
            self._current_stitch = 1
        elif self._current_stitch > self.num_stitches:
            self._current_stitch = self.num_stitches

    def stop_if_at_end(self) -> None:
        if self.direction == -1 and self._current_stitch == 1:
            self.stop()
        elif self.direction == 1 and self._current_stitch == self.num_stitches:
            self.stop()

    def start_if_not_at_end(self) -> None:
        if self.direction == -1 and self._current_stitch > 1:
            self.go()
        elif self.direction == 1 and self._current_stitch < self.num_stitches:
            self.go()

    def animate(self, event: Optional[wx.TimerEvent] = None) -> None:
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
        self.set_current_stitch(self._current_stitch + self.direction * stitch_increment)

    def clear(self) -> None:
        self.loaded = False
        self.Refresh()

    def load(self, stitch_plan: StitchPlan) -> None:
        self._current_stitch = 1.0
        self.direction = 1
        self.minx, self.miny, self.maxx, self.maxy = stitch_plan.bounding_box
        self.width = self.maxx - self.minx
        self.height = self.maxy - self.miny
        self.dimensions_mm = stitch_plan.dimensions_mm
        self.num_stitches = stitch_plan.num_stitches
        self.num_trims = stitch_plan.num_trims
        self.num_color_changes = stitch_plan.num_color_blocks - 1
        self.num_stops = stitch_plan.num_stops
        self.num_jumps = stitch_plan.num_jumps - 1
        self.parse_stitch_plan(stitch_plan)
        self.choose_zoom_and_pan()
        self.set_current_stitch(0)

        self.set_status_bar(
            _("Dimensions: {:.2f} x {:.2f}").format(
                stitch_plan.dimensions_mm[0],
                stitch_plan.dimensions_mm[1]
            ),
            1
        )

        self.loaded = True

        if self.renderer is None:
            self.renderer = SimpleDrawingPanel(self, self, stitch_plan)

            self.renderer.Bind(wx.EVT_LEFT_DOWN, self.on_left_mouse_button_down)
            self.renderer.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)

            self.sizer.Add(self.renderer, 1, wx.EXPAND)
            self.sizer.Layout()
            self.Layout()
            self.Refresh()
        else:
            self.renderer.set_stitch_plan(stitch_plan)

        if hasattr(self.view_panel, 'info_panel') and self.view_panel.info_panel is not None:
            self.view_panel.info_panel.update()

    def set_status_bar(self, msg: str, pos: int) -> None:
        """
        Set a status bar field on the top level parent, if it exists.
        This probably belongs with that top level parent that creates the status bar instead of here.
        """
        tlp = self.GetTopLevelParent()
        if isinstance(tlp, wx.Frame):
            statusbar = tlp.GetStatusBar()
            if statusbar is not None:
                statusbar.SetStatusText(msg, pos)

    def parse_stitch_plan(self, stitch_plan: StitchPlan) -> None:
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

    def set_page_specs(self, page_specs) -> None:
        self.SetBackgroundColour(page_specs['desk_color'])
        self.page_specs = page_specs

    def set_background_color(self, color: wx.Colour) -> None:
        self.background_color = color

    def set_show_page(self, show_page: bool) -> None:
        self.show_page = show_page

    def choose_zoom_and_pan(self) -> None:
        # ignore if EVT_SIZE fired before we load the stitch plan
        if not self.width and not self.height:
            return

        # types-wxpython 0.9.7 incorrectly says GetClientSize() has type Rect (???)
        size = cast(wx.Size, self.GetClientSize())

        # add some padding to make stitches at the edge more visible
        width_ratio = size.width / float(self.width + 10)
        height_ratio = size.height / float(self.height + 10)
        self.zoom = max(min(width_ratio, height_ratio), 0.01)

        # center the design
        self.pan = ((size.width - self.zoom * self.width) / 2.0,
                    (size.height - self.zoom * self.height) / 2.0)

    def stop(self) -> None:
        self.animating = False
        self.timer.Stop()
        self.control_panel.on_stop()

    def go(self) -> None:
        if not self.loaded:
            return

        if not self.animating:
            try:
                self.animating = True
                self.last_frame_start = 0
                self.timer.Start(int(self.target_frame_period * 1000))
                self.animate()
                self.control_panel.on_start()
            except RuntimeError:
                pass

    def set_speed(self, speed: int) -> None:
        self.speed = speed
        global_settings['simulator_speed'] = speed

    def forward(self) -> None:
        self.direction = 1
        self.start_if_not_at_end()

    def reverse(self) -> None:
        self.direction = -1
        self.start_if_not_at_end()

    def set_current_stitch(self, stitch: float) -> None:
        self._current_stitch = stitch
        self.clamp_current_stitch()
        try:
            command = self.commands[int(self._current_stitch)]
        except IndexError:
            # no stitch plan loaded yet, do nothing for now
            return
        self.control_panel.on_current_stitch(int(self._current_stitch), command)
        self.set_status_bar(_("Command: %s") % COMMAND_NAMES[command], 2)
        self.stop_if_at_end()
        self.Refresh()

    def restart(self) -> None:
        if self.direction == 1:
            self._current_stitch = 1
        elif self.direction == -1:
            self._current_stitch = self.num_stitches

        self.go()

    def one_stitch_forward(self) -> None:
        self.set_current_stitch(self._current_stitch + 1)

    def one_stitch_backward(self) -> None:
        self.set_current_stitch(self._current_stitch - 1)

    def on_left_mouse_button_down(self, event: wx.MouseEvent) -> None:
        obj = event.GetEventObject()
        if self.loaded:
            obj.CaptureMouse()
            self.drag_start = event.GetPosition()
            self.drag_original_pan = self.pan
            obj.Bind(wx.EVT_MOTION, self.on_drag)
            obj.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.on_drag_end)
            obj.Bind(wx.EVT_LEFT_UP, self.on_drag_end)

    def on_drag(self, event: wx.MouseEvent) -> None:
        obj = event.GetEventObject()
        if obj.HasCapture() and event.Dragging():
            delta = event.GetPosition()
            offset = (
                delta.x - self.drag_start[0],
                delta.y - self.drag_start[1]
            )
            self.pan = (self.drag_original_pan[0] + offset[0], self.drag_original_pan[1] + offset[1])
            self.Refresh()

    def on_drag_end(self, event: wx.MouseEvent) -> None:
        obj = event.GetEventObject()
        if obj.HasCapture():
            obj.ReleaseMouse()

        obj.Unbind(wx.EVT_MOTION)
        obj.Unbind(wx.EVT_MOUSE_CAPTURE_LOST)
        obj.Unbind(wx.EVT_LEFT_UP)

    def on_mouse_wheel(self, event: wx.MouseEvent) -> None:
        if event.GetWheelRotation() > 0:
            zoom_delta = 1.03
        else:
            zoom_delta = 0.97

        # If we just change the zoom, the design will appear to move on the
        # screen.  We have to adjust the pan to compensate.  We want to keep
        # the part of the design under the mouse pointer in the same spot
        # after we zoom, so that we appear to be zooming centered on the
        # mouse pointer.

        # This will create a matrix that takes a point in the design and
        # converts it to screen coordinates:
        matrix = wx.AffineMatrix2D()
        matrix.Translate(*self.pan)
        matrix.Scale(self.zoom, self.zoom)

        # First, figure out where the mouse pointer is in the coordinate system
        # of the design:
        pos = event.GetPosition()
        inverse_matrix = wx.AffineMatrix2D()
        inverse_matrix.Set(*matrix.Get())
        inverse_matrix.Invert()
        pos = inverse_matrix.TransformPoint(*pos)

        # Next, see how that point changes position on screen before and after
        # we apply the zoom change:
        x_old, y_old = matrix.TransformPoint(*pos)
        matrix.Scale(zoom_delta, zoom_delta)
        x_new, y_new = matrix.TransformPoint(*pos)
        x_delta = x_new - x_old
        y_delta = y_new - y_old

        # Finally, compensate for that change in position:
        self.pan = (self.pan[0] - x_delta, self.pan[1] - y_delta)

        self.zoom *= zoom_delta

        self.Refresh()

    @property
    def current_stitch(self) -> int:
        return int(self._current_stitch)

    @property
    def draw_cursor(self) -> bool:
        return self.view_panel.btnCursor.GetValue()

    @property
    def render_jumps(self) -> bool:
        return self.view_panel.btnJump.GetValue()

    @property
    def render_needle_pen_points(self) -> bool:
        return self.view_panel.btnNpp.GetValue()
