execfile('inkstitch_activate_venv.py')

import sys
import os
import numpy
import wx
import inkex
import simplestyle
import colorsys

from embroider import patches_to_stitches, stitches_to_polylines, PIXELS_PER_MM

class EmbroiderySimulator(wx.Frame):
    def __init__(self, *args, **kwargs):
        stitch_file = kwargs.pop('stitch_file', None)
        patches = kwargs.pop('patches', None)
        self.on_close_hook = kwargs.pop('on_close', None)
        self.frame_period = kwargs.pop('frame_period', 80)
        self.stitches_per_frame = kwargs.pop('stitches_per_frame', 1)
        self.target_duration = kwargs.pop('target_duration', None)

        screen_rect = wx.Display(0).ClientArea
        self.max_width = kwargs.pop('max_width', screen_rect.GetWidth())
        self.max_height = kwargs.pop('max_height', screen_rect.GetHeight())
        self.scale = 1

        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetFocus()

        self.load(stitch_file, patches)

        if self.target_duration:
            self.adjust_speed(self.target_duration)

        self.buffer = wx.Bitmap(self.width * self.scale, self.height * self.scale)
        self.dc = wx.MemoryDC()
        self.dc.SelectObject(self.buffer)
        self.canvas = wx.GraphicsContext.Create(self.dc)

        self.clear()

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        self.timer = None

        self.last_pos = None

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def load(self, stitch_file=None, patches=None):
        if stitch_file:
            self.mirror = True
            self.segments = self._parse_stitch_file(stitch_file)
        elif patches:
            self.mirror = False
            self.segments = self._patches_to_segments(patches)
        else:
            return

        self.trim_margins()
        self.calculate_dimensions()

    def adjust_speed(self, duration):
        self.frame_period = 1000 * float(duration) / len(self.segments)
        self.stitches_per_frame = 1

        while self.frame_period < 1.0:
            self.frame_period *= 2
            self.stitches_per_frame *= 2

    def on_key_down(self, event):
        keycode = event.GetKeyCode()

        if keycode == ord("+") or keycode == ord("=") or keycode == wx.WXK_UP:
            if self.frame_period == 1:
                self.stitches_per_frame *= 2
            else:
                self.frame_period = self.frame_period / 2
        elif keycode == ord("-") or keycode == ord("_") or keycode == wx.WXK_DOWN:
            if self.stitches_per_frame == 1:
                self.frame_period *= 2
            else:
                self.stitches_per_frame /= 2
        elif keycode == ord("Q"):
            self.Close()
        elif keycode == ord('P'):
            if self.timer.IsRunning():
                self.timer.Stop()
            else:
                self.timer.Start(self.frame_period)
        elif keycode == ord("R"):
            self.stop()
            self.clear()
            self.go()

        self.frame_period = max(1, self.frame_period)
        self.stitches_per_frame = max(self.stitches_per_frame, 1)

        if self.timer.IsRunning():
            self.timer.Stop()
            self.timer.Start(self.frame_period)

    def _strip_quotes(self, string):
        if string.startswith('"') and string.endswith('"'):
            string = string[1:-1]

        return string

    def color_to_pen(self, color):
        # python colorsys module uses floats from 0 to 1.0
        color = [value / 255.0 for value in color]

        hls = list(colorsys.rgb_to_hls(*color))

        # Our background is white.  If the color is too close to white, then
        # it won't be visible.  Capping lightness should make colors visible
        # without changing them too much.
        hls[1] = min(hls[1], 0.85)

        color = colorsys.hls_to_rgb(*hls)

        # convert back to values in the range of 0-255
        color = [value * 255 for value in color]

        return wx.Pen(color)

    def _patches_to_segments(self, patches):
        stitches = patches_to_stitches(patches)

        segments = []

        last_pos = None
        last_color = None
        pen = None

        for stitch in stitches:
            pos = (stitch.x, stitch.y)

            if stitch.color == last_color:
                segments.append(((last_pos, pos), pen))
            else:
                pen = self.color_to_pen(simplestyle.parseColor(stitch.color))

            last_pos = pos
            last_color = stitch.color

        return segments

    def _parse_stitch_file(self, stitch_file_path):
        # "$","1","229","229","229","(null)","(null)"
        # "*","JUMP","1.595898","48.731899"
        # "*","STITCH","1.595898","48.731899"

        segments = []

        pos = (0, 0)
        pen = wx.Pen('black')
        cut = True

        with open(stitch_file_path) as stitch_file:
            for line in stitch_file:
                fields = line.strip().split(",")
                fields = [self._strip_quotes(field) for field in fields]

                symbol, command = fields[:2]

                if symbol == "$":
                    red, green, blue = fields[2:5]
                    pen = self.color_to_pen((int(red), int(green), int(blue)))
                elif symbol == "*":
                    if command == "COLOR":
                        # change color
                        # The next command should be a JUMP, and we'll need to skip stitching.
                        cut = True
                    elif command == "JUMP" or command == "STITCH":
                        # JUMP just means a long stitch, really.

                        x, y = fields[2:]
                        new_pos = (float(x) * PIXELS_PER_MM, float(y) * PIXELS_PER_MM)

                        if not cut:
                            segments.append(((pos, new_pos), pen))

                        cut = False
                        pos = new_pos

        return segments

    def all_coordinates(self):
        for segment in self.segments:
            start, end = segment[0]

            yield start
            yield end

    def trim_margins(self):
        """remove any unnecessary whitespace around the design"""

        min_x = sys.maxint
        min_y = sys.maxint

        for x, y in self.all_coordinates():
            min_x = min(min_x, x)
            min_y = min(min_y, y)

        new_segments = []

        for segment in self.segments:
            (start, end), color = segment

            new_segment = (
                           (
                            (start[0] - min_x, start[1] - min_y),
                            (end[0] - min_x, end[1] - min_y),
                           ),
                           color
                          )

            new_segments.append(new_segment)

        self.segments = new_segments

    def calculate_dimensions(self):
        width = 0
        height = 0

        for x, y in self.all_coordinates():
            width = max(width, x)
            height = max(height, y)

        self.width = width
        self.height = height
        self.scale = min(float(self.max_width) / width, float(self.max_height) / height)

        # make room for decorations and a bit of a margin
        self.scale *= 0.95

    def go(self):
        self.clear()

        self.current_stitch = 0

        if not self.timer:
            self.timer = wx.PyTimer(self.draw_one_frame)

        self.timer.Start(self.frame_period)

    def on_close(self, event):
        self.stop()

        if self.on_close_hook:
            self.on_close_hook()

        self.Destroy()

    def stop(self):
        if self.timer:
            self.timer.Stop()

    def clear(self):
        self.dc.SetBackground(wx.Brush('white'))
        self.dc.Clear()
        self.last_pos = None
        self.Refresh()

    def on_size(self, e):
        # ensure that the whole canvas is visible
        window_width, window_height = self.GetSize()
        client_width, client_height = self.GetClientSize()

        decorations_width = window_width - client_width
        decorations_height = window_height - client_height

        self.SetSize((self.width * self.scale + decorations_width, self.height * self.scale + decorations_height))

        e.Skip()

    def on_paint(self, e):
        dc = wx.PaintDC(self.panel)
        dc.DrawBitmap(self.buffer, 0, 0)

        if self.last_pos:
            dc.DrawLine(self.last_pos[0] - 10, self.last_pos[1],      self.last_pos[0] + 10, self.last_pos[1])
            dc.DrawLine(self.last_pos[0],      self.last_pos[1] - 10, self.last_pos[0],      self.last_pos[1] + 10)

    def redraw(self):
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.buffer, 0, 0)

    def draw_one_frame(self):
        for i in xrange(self.stitches_per_frame):
            try:
                ((x1, y1), (x2, y2)), color = self.segments[self.current_stitch]

                if self.mirror:
                    y1 = self.height - y1
                    y2 = self.height - y2

                x1 = x1 * self.scale
                y1 = y1 * self.scale
                x2 = x2 * self.scale
                y2 = y2 * self.scale

                self.canvas.SetPen(color)
                self.canvas.DrawLines(((x1, y1), (x2, y2)))
                self.Refresh()

                self.current_stitch += 1
                self.last_pos = (x2, y2)
            except IndexError:
                self.timer.Stop()

class SimulateEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-P", "--path",
                                     action="store", type="string",
                                     dest="path", default=".",
                                     help="Directory in which to store output file")

    def effect(self):
        app = wx.App()
        frame = EmbroiderySimulator(None, -1, "Embroidery Simulation", wx.DefaultPosition, size=(1000, 1000), stitch_file=self.get_stitch_file())
        app.SetTopWindow(frame)
        frame.Show()
        wx.CallAfter(frame.go)
        app.MainLoop()

    def get_stitch_file(self):
        svg_filename = self.document.getroot().get(inkex.addNS('docname', 'sodipodi'))
        csv_filename = svg_filename.replace('.svg', '.csv')
        stitch_file = os.path.join(self.options.path, csv_filename)

        return stitch_file


if __name__ == "__main__":
    effect = SimulateEffect()
    effect.affect()
    sys.exit(0)
