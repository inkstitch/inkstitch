#!/usr/bin/python
#

import sys
import traceback
import os

import inkex
import inkstitch
from inkstitch import _, PIXELS_PER_MM, SVG_GROUP_TAG
from inkstitch.extensions import InkstitchExtension
from inkstitch.stitch_plan import patches_to_stitch_plan
from inkstitch.svg import render_stitch_plan

from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import wx, wx.html2

class PrintPreview(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        self.browser.RegisterHandler(wx.html2.WebViewFSHandler('memory'))
        #self.browser.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.error)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((1280, 800))
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Destroy()


def datetimeformat(value, format='%Y/%m/%d'):
    return value.strftime(format)

class Print(InkstitchExtension):
    def build_environment(self):
        if getattr( sys, 'frozen', False ) :
            template_dir = os.path.join(sys._MEIPASS, "templates")
        else:
            template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")

        env = Environment(
            loader = FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            # extensions=['jinja2.ext.i18n']
        )

        env.filters['datetimeformat'] = datetimeformat

        return env

    def strip_namespaces(self):
        # namespace prefixes seem to trip up HTML, so get rid of them
        for element in self.document.iter():
            if element.tag[0]=='{':
                element.tag = element.tag[element.tag.index('}',1) + 1:]

    def effect(self):
        if not self.get_elements():
            return

        self.hide_all_layers()

        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches)
        render_stitch_plan(self.document.getroot(), stitch_plan)

        self.strip_namespaces()

        # Now the stitch plan layer will contain a set of groups, each
        # corresponding to a color block.  We'll create a set of SVG files
        # corresponding to each individual color block and a final one
        # for all color blocks together.

        svg = self.document.getroot()
        layers = svg.findall("./g[@{http://www.inkscape.org/namespaces/inkscape}groupmode='layer']")
        stitch_plan_layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")

        # First, delete all of the other layers.  We don't need them and they'll
        # just bulk up the SVG.
        for layer in layers:
            if layer is not stitch_plan_layer:
                svg.remove(layer)

        overview_svg = inkex.etree.tostring(self.document)

        color_block_groups = stitch_plan_layer.getchildren()

        for i, group in enumerate(color_block_groups):
            # clear the stitch plan layer
            del stitch_plan_layer[:]

            # add in just this group
            stitch_plan_layer.append(group)

            # save an SVG preview
            stitch_plan.color_blocks[i].svg_preview = inkex.etree.tostring(self.document)

        env = self.build_environment()
        template = env.get_template('index.html')

        html = template.render(
            view = {'overview': True, 'detailedview': True},
            logo = {'src' : 'test.png', 'title' : 'LOGO'},
            date = date.today(),
            client = "The name of the long client name thing",
            job = {'title' : 'TITLE OF THE JOB LONG NAME THING', 'totalcolors' : '000', 'totalstops' : '000', 'totaltrims' : '000', 'size' : '0000 x 0000', 'stitchcount' : '000 000 000', 'totalthread' : '000 000 000', 'estimatedtime' : '00h00 @ 000mm/s'},
            svg_complete = overview_svg,
            svg_scale = '1/1',
            color_blocks = stitch_plan.color_blocks,
            num_pages = '2',
        )

        self.show_print_preview(html)

        # don't let inkex print the document out
        sys.exit(0)

    def show_print_preview(self, html):
        app = wx.App()
        print_preview = PrintPreview(None, -1)
        print_preview.browser.SetPage(html, "about:print")
        print_preview.Show()
        wx.CallLater(3000, print_preview.browser.Print)
        app.SetTopWindow(print_preview)
        app.MainLoop()


if __name__ == '__main__':
    effect = Print()
    effect.affect()
