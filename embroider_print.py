#!/usr/bin/python
#

import sys
import traceback
import os
from threading import Thread
import socket
import errno
import time
import logging

import inkex
import inkstitch
from inkstitch import _, PIXELS_PER_MM, SVG_GROUP_TAG
from inkstitch.extensions import InkstitchExtension
from inkstitch.stitch_plan import patches_to_stitch_plan
from inkstitch.svg import render_stitch_plan

from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import base64

from flask import Flask, request, Response, send_from_directory
import webbrowser
import requests


def datetimeformat(value, format='%Y/%m/%d'):
    return value.strftime(format)


def open_url(url):
    # Avoid spurious output from xdg-open.  Not only will the user see
    # anything on stderr, but any output on stdout will crash inkscape.
    null = open(os.devnull, 'w')
    old_stdout = os.dup(sys.stdout.fileno())
    old_stderr = os.dup(sys.stderr.fileno())
    os.dup2(null.fileno(), sys.stdout.fileno())
    os.dup2(null.fileno(), sys.stderr.fileno())

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
    os.dup2(old_stderr, sys.stderr.fileno())
    os.close(old_stdout)
    os.close(old_stderr)


class PrintPreviewServer(Thread):
    def __init__(self, *args, **kwargs):
        self.html = kwargs.pop('html')
        Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.last_request_time = None
        self.shutting_down = False

        self.__setup_app()

    def __set_resources_path(self):
        if getattr(sys, 'frozen', False):
            self.resources_path = os.path.join(sys._MEIPASS, 'print', 'resources')
        else:
            self.resources_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'print', 'resources')

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
            return 'Server shutting down...'

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

    def watch(self):
        try:
            while True:
                time.sleep(1)
                if self.shutting_down:
                    break

                if self.last_request_time is not None and \
                    (time.time() - self.last_request_time) > 4:
                        # for whatever reason, shutting down only seems possible in
                        # the context of a flask request, so we'll just make one
                        r = requests.post("http://%s:%s/shutdown" % (self.host, self.port))
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



class Print(InkstitchExtension):
    def build_environment(self):
        if getattr( sys, 'frozen', False ) :
            template_dir = os.path.join(sys._MEIPASS, "print", "templates")
        else:
            template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "print", "templates")

        env = Environment(
            loader = FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            extensions=['jinja2.ext.i18n']
        )

        env.filters['datetimeformat'] = datetimeformat
        env.install_gettext_translations(inkstitch.translation)

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
            view = {'client_overview': True, 'client_detailedview': True, 'operator_overview': False, 'operator_detailedview': False},
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
            svg_scale = '100%',
            color_blocks = stitch_plan.color_blocks,
        )

        print_preview_server = PrintPreviewServer(html=html)
        print_preview_server.start()

        time.sleep(1)
        open_url("http://%s:%s/" % (print_preview_server.host, print_preview_server.port))
        print_preview_server.join()

        # don't let inkex print the document out
        sys.exit(0)

    def show_print_preview(self, html):
        cef.Initialize()

        self.browser = cef.CreateBrowserSync(url=html_to_data_uri(html), window_title='Ink/Stitch Print Preview')
        threading.Timer(3.0, self.browser.Print).start()
        cef.MessageLoop()
        cef.Shutdown()

if __name__ == '__main__':
    effect = Print()
    effect.affect()
