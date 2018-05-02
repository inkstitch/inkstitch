import sys
import traceback
import os
from threading import Thread
import socket
import errno
import time
import logging
from copy import deepcopy
import wx
import appdirs
import json
import inkex
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import base64
from flask import Flask, request, Response, send_from_directory, jsonify
import webbrowser
import requests

from .base import InkstitchExtension
from ..i18n import _, translation as inkstitch_translation
from ..svg import PIXELS_PER_MM, render_stitch_plan
from ..svg.tags import SVG_GROUP_TAG
from ..stitch_plan import patches_to_stitch_plan
from ..threads import ThreadCatalog


def datetimeformat(value, format='%Y/%m/%d'):
    return value.strftime(format)


def defaults_path():
    defaults_dir = appdirs.user_config_dir('inkstitch')

    if not os.path.exists(defaults_dir):
        os.makedirs(defaults_dir)

    return os.path.join(defaults_dir, 'print_settings.json')


def load_defaults():
    try:
        with open(defaults_path(), 'r') as defaults_file:
            defaults = json.load(defaults_file)
            return defaults
    except:
        return {}


def save_defaults(defaults):
    with open(defaults_path(), 'w') as defaults_file:
        json.dump(defaults, defaults_file)


def open_url(url):
    # Avoid spurious output from xdg-open.  Any output on stdout will crash
    # inkscape.
    null = open(os.devnull, 'w')
    old_stdout = os.dup(sys.stdout.fileno())
    os.dup2(null.fileno(), sys.stdout.fileno())

    if getattr(sys, 'frozen', False):

        # PyInstaller sets LD_LIBRARY_PATH.  We need to temporarily clear it
        # to avoid confusing xdg-open, which webbrowser will run.

        # The following code is adapted from PyInstaller's documentation
        # http://pyinstaller.readthedocs.io/en/stable/runtime-information.html

        old_environ = dict(os.environ)  # make a copy of the environment
        lp_key = 'LD_LIBRARY_PATH'  # for Linux and *BSD.
        lp_orig = os.environ.get(lp_key + '_ORIG')  # pyinstaller >= 20160820 has this
        if lp_orig is not None:
            os.environ[lp_key] = lp_orig  # restore the original, unmodified value
        else:
            os.environ.pop(lp_key, None)  # last resort: remove the env var

        webbrowser.open(url)

        # restore the old environ
        os.environ.clear()
        os.environ.update(old_environ)
    else:
        webbrowser.open(url)

    # restore file descriptors
    os.dup2(old_stdout, sys.stdout.fileno())
    os.close(old_stdout)


class PrintPreviewServer(Thread):
    def __init__(self, *args, **kwargs):
        self.html = kwargs.pop('html')
        self.metadata = kwargs.pop('metadata')
        self.stitch_plan = kwargs.pop('stitch_plan')
        Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.last_request_time = None
        self.shutting_down = False

        self.__setup_app()

    def __set_resources_path(self):
        if getattr(sys, 'frozen', False):
            self.resources_path = os.path.join(sys._MEIPASS, 'print', 'resources')
        else:
            self.resources_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'print', 'resources'))

    def __setup_app(self):
        self.__set_resources_path()
        self.app = Flask(__name__)

        @self.app.before_request
        def request_started():
            self.last_request_time = time.time()

        @self.app.before_first_request
        def start_watcher():
            self.watcher_thread = Thread(target=self.watch)
            self.watcher_thread.daemon = True
            self.watcher_thread.start()

        @self.app.route('/')
        def index():
            return self.html

        @self.app.route('/shutdown', methods=['POST'])
        def shutdown():
            self.shutting_down = True
            request.environ.get('werkzeug.server.shutdown')()
            return _('Closing...') + '<br/><br/>' + _('It is safe to close this window now.')

        @self.app.route('/resources/<path:resource>', methods=['GET'])
        def resources(resource):
            return send_from_directory(self.resources_path, resource, cache_timeout=1)

        @self.app.route('/ping')
        def ping():
            # Javascript is letting us know it's still there.  This resets self.last_request_time.
            return "pong"

        @self.app.route('/printing/start')
        def printing_start():
            # temporarily turn off the watcher while the print dialog is up,
            # because javascript will be frozen
            self.last_request_time = None
            return "OK"

        @self.app.route('/printing/end')
        def printing_end():
            # nothing to do here -- request_started() will restart the watcher
            return "OK"

        @self.app.route('/settings/<field_name>', methods=['POST'])
        def set_field(field_name):
            self.metadata[field_name] = request.json['value']
            return "OK"

        @self.app.route('/settings/<field_mame>', methods=['GET'])
        def get_field(field_name):
            return jsonify(self.metadata[field_name])

        @self.app.route('/settings', methods=['GET'])
        def get_settings():
            settings = {}
            settings.update(load_defaults())
            settings.update(self.metadata)
            return jsonify(settings)

        @self.app.route('/defaults', methods=['POST'])
        def set_defaults():
            save_defaults(request.json['value'])
            return "OK"

        @self.app.route('/palette', methods=['POST'])
        def set_palette():
            name = request.json['name']
            catalog = ThreadCatalog()
            palette = catalog.get_palette_by_name(name)
            catalog.apply_palette(self.stitch_plan, palette)

            # clear any saved color or thread names
            for field in self.metadata:
                if field.startswith('color-') or field.startswith('thread-'):
                    del self.metadata[field]

            self.metadata['thread-palette'] = name

            return "OK"

        @self.app.route('/threads', methods=['GET'])
        def get_threads():
            threads = []
            for color_block in self.stitch_plan:
                threads.append({
                                'hex': color_block.color.hex_digits,
                                'name': color_block.color.name,
                                'manufacturer': color_block.color.manufacturer,
                                'number': color_block.color.number,
                             })

            return jsonify(threads)

    def stop(self):
        # for whatever reason, shutting down only seems possible in
        # the context of a flask request, so we'll just make one
        requests.post("http://%s:%s/shutdown" % (self.host, self.port))

    def watch(self):
        try:
            while True:
                time.sleep(1)
                if self.shutting_down:
                    break

                if self.last_request_time is not None and \
                    (time.time() - self.last_request_time) > 3:
                        self.stop()
                        break
        except:
            # seems like sometimes this thread blows up during shutdown
            pass

    def disable_logging(self):
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

    def run(self):
        self.disable_logging()

        self.host = "127.0.0.1"
        self.port = 5000

        while True:
            try:
                self.app.run(self.host, self.port, threaded=True)
            except socket.error, e:
                if e.errno == errno.EADDRINUSE:
                    self.port += 1
                    continue
                else:
                    raise
            else:
                break


class PrintInfoFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.print_server = kwargs.pop("print_server")
        wx.Frame.__init__(self, *args, **kwargs)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        text = wx.StaticText(panel, label=_("A print preview has been opened in your web browser.  This window will stay open in order to communicate with the JavaScript code running in your browser.\n\nThis window will close after you close the print preview in your browser, or you can close it manually if necessary."))
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        text.SetFont(font)
        sizer.Add(text, proportion=1, flag=wx.ALL|wx.EXPAND, border=20)

        stop_button = wx.Button(panel, id=wx.ID_CLOSE)
        stop_button.Bind(wx.EVT_BUTTON, self.close_button_clicked)
        sizer.Add(stop_button, proportion=0, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        panel.SetSizer(sizer)
        panel.Layout()

        self.timer = wx.PyTimer(self.__watcher)
        self.timer.Start(250)

    def close_button_clicked(self, event):
        self.print_server.stop()

    def __watcher(self):
        if not self.print_server.is_alive():
            self.timer.Stop()
            self.timer = None
            self.Destroy()


class Print(InkstitchExtension):
    def build_environment(self):
        if getattr( sys, 'frozen', False ) :
            template_dir = os.path.join(sys._MEIPASS, "print", "templates")
        else:
            template_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "print", "templates"))

        env = Environment(
            loader = FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            extensions=['jinja2.ext.i18n']
        )

        env.filters['datetimeformat'] = datetimeformat
        env.install_gettext_translations(inkstitch_translation)

        return env

    def strip_namespaces(self):
        # namespace prefixes seem to trip up HTML, so get rid of them
        for element in self.document.iter():
            if element.tag[0]=='{':
                element.tag = element.tag[element.tag.index('}',1) + 1:]

    def effect(self):
        # It doesn't really make sense to print just a couple of selected
        # objects.  It's almost certain they meant to print the whole design.
        # If they really wanted to print just a few objects, they could set
        # the rest invisible temporarily.
        self.selected = {}

        if not self.get_elements():
            return

        self.hide_all_layers()

        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches)
        palette = ThreadCatalog().match_and_apply_palette(stitch_plan, self.get_inkstitch_metadata()['thread-palette'])
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
            view = {'client_overview': False, 'client_detailedview': False, 'operator_overview': True, 'operator_detailedview': True},
            logo = {'src' : '', 'title' : 'LOGO'},
            date = date.today(),
            client = "",
            job = {
                    'title': '',
                    'num_colors': stitch_plan.num_colors,
                    'num_color_blocks': len(stitch_plan),
                    'num_stops': stitch_plan.num_stops,
                    'num_trims': stitch_plan.num_trims,
                    'dimensions': stitch_plan.dimensions_mm,
                    'num_stitches': stitch_plan.num_stitches,
                    'estimated_time': '', # TODO
                    'estimated_thread': '', # TODO
                  },
            svg_overview = overview_svg,
            color_blocks = stitch_plan.color_blocks,
            palettes = ThreadCatalog().palette_names(),
            selected_palette = palette.name,
        )

        # We've totally mucked with the SVG.  Restore it so that we can save
        # metadata into it.
        self.document = deepcopy(self.original_document)

        print_server = PrintPreviewServer(html=html, metadata=self.get_inkstitch_metadata(), stitch_plan=stitch_plan)
        print_server.start()

        time.sleep(1)
        open_url("http://%s:%s/" % (print_server.host, print_server.port))

        app = wx.App()
        info_frame = PrintInfoFrame(None, title=_("Ink/Stitch Print"), size=(450, 350), print_server=print_server)
        info_frame.Show()
        app.MainLoop()
