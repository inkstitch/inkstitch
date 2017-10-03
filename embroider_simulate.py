import sys
import os
import numpy
import wx
from wx.lib.floatcanvas.FloatCanvas import FloatCanvas
import inkex

class EmbroiderySimulator(wx.Frame):
    def __init__(self, *args, **kwargs):
        stitch_file = kwargs.pop('stitch_file')
        self.frame_period = kwargs.pop('frame_period', 10)
        self.stitches_per_frame = kwargs.pop('stitches_per_frame', 1)

        wx.Frame.__init__(self, *args, **kwargs)
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetFocus()

        self.stitches = self._parse_stitches(stitch_file)
        self.width, self.height = self.get_dimensions()

        self.buffer = wx.EmptyBitmap(self.width, self.height)
        self.dc = wx.MemoryDC()
        self.dc.SelectObject(self.buffer)
        self.canvas = wx.GraphicsContext.Create(self.dc)

        self.clear()

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        self.last_pos = None

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

        self.frame_period = max(1, self.frame_period)
        self.stitches_per_frame = max(self.stitches_per_frame, 1)

        if self.timer.IsRunning():
            self.timer.Stop()
            self.timer.Start(self.frame_period)

    def _strip_quotes(self, string):
        if string.startswith('"') and string.endswith('"'):
            string = string[1:-1]

        return string

    def _parse_stitches(self, stitch_file_path):
        # "$","1","229","229","229","(null)","(null)"
        # "*","JUMP","1.595898","48.731899"
        # "*","STITCH","1.595898","48.731899"

        stitches = []

        pos = (0, 0)
        color = wx.Brush('black')
        cut = True

        with open(stitch_file_path) as stitch_file:
            for line in stitch_file:
                fields = line.strip().split(",")
                fields = [self._strip_quotes(field) for field in fields]

                symbol, command = fields[:2]

                if symbol == "$":
                    red, green, blue = fields[2:5]
                    color = wx.Pen((int(red), int(green), int(blue)))
                elif symbol == "*":
                    if command == "COLOR":
                        # change color
                        # The next command should be a JUMP, and we'll need to skip stitching.
                        cut = True
                    elif command == "JUMP" or command == "STITCH":
                        # JUMP just means a long stitch, really.

                        x, y = fields[2:]
                        new_pos = (int(float(x) * 10), int(float(y) * 10))

                        if not cut:
                            stitches.append(((pos, new_pos), color))

                        cut = False
                        pos = new_pos

        return stitches

    def get_dimensions(self):
        width = 0
        height = 0

        for stitch in self.stitches:
            (start_x, start_y), (end_x, end_y) = stitch[0]

            width = max(width, start_x, end_x)
            height = max(height, start_y, end_y)

        return width, height

    def go(self):
        self.current_stitch = 0
        self.timer = wx.PyTimer(self.draw_one_stitch)
        self.timer.Start(self.frame_period)

    def clear(self):
        self.dc.SetBackground(wx.Brush('white'))
        self.dc.Clear()

    def on_size(self, e):
        # ensure that the whole canvas is visible
        window_width, window_height = self.GetSize()
        client_width, client_height = self.GetClientSize()

        decorations_width = window_width - client_width
        decorations_height = window_height - client_height

        self.SetSize((self.width + decorations_width, self.height + decorations_height))

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

    def draw_one_stitch(self):
        for i in xrange(self.stitches_per_frame):
            try:
                ((x1, y1), (x2, y2)), color = self.stitches[self.current_stitch]
                y1 = self.height - y1
                y2 = self.height - y2

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
