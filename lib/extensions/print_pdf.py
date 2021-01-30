import errno
import json
import logging
import os
import socket
import sys
import time
from copy import deepcopy
from datetime import date
from threading import Thread

import appdirs
import requests
from flask import Flask, Response, jsonify, request, send_from_directory
from jinja2 import Environment, FileSystemLoader, select_autoescape
from lxml import etree

from ..gui import open_url
from ..i18n import translation as inkstitch_translation
from ..stitch_plan import patches_to_stitch_plan
from ..svg import render_stitch_plan
from ..svg.tags import INKSCAPE_GROUPMODE
from ..threads import ThreadCatalog
from .base import InkstitchExtension


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
    except BaseException:
        return {}


def save_defaults(defaults):
    with open(defaults_path(), 'w') as defaults_file:
        json.dump(defaults, defaults_file)


class PrintPreviewServer(Thread):
    def __init__(self, *args, **kwargs):
        self.html = kwargs.pop('html')
        self.metadata = kwargs.pop('metadata')
        self.stitch_plan = kwargs.pop('stitch_plan')
        self.realistic_overview_svg = kwargs.pop('realistic_overview_svg')
        self.realistic_color_block_svgs = kwargs.pop('realistic_color_block_svgs')
        Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.shutting_down = False

        self.__setup_app()

    def __set_resources_path(self):
        if getattr(sys, 'frozen', False):
            self.resources_path = os.path.join(sys._MEIPASS, 'print', 'resources')
        else:
            self.resources_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'print', 'resources'))

    def __setup_app(self):  # noqa: C901
        self.__set_resources_path()

        # Disable warning about using a development server in a production environment
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None

        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            return self.html

        @self.app.route('/shutdown', methods=['POST'])
        def shutdown():
            self.shutting_down = True
            request.environ.get('werkzeug.server.shutdown')()
            return "shutting down"

        @self.app.route('/resources/<path:resource>', methods=['GET'])
        def resources(resource):
            return send_from_directory(self.resources_path, resource, cache_timeout=1)

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

        @self.app.route('/realistic/block<int:index>', methods=['GET'])
        def get_realistic_block(index):
            return Response(self.realistic_color_block_svgs[index], mimetype='image/svg+xml')

        @self.app.route('/realistic/overview', methods=['GET'])
        def get_realistic_overview():
            return Response(self.realistic_overview_svg, mimetype='image/svg+xml')

    def stop(self):
        # for whatever reason, shutting down only seems possible in
        # the context of a flask request, so we'll just make one
        requests.post("http://%s:%s/shutdown" % (self.host, self.port))

    def disable_logging(self):
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

    def run(self):
        self.disable_logging()

        self.host = "127.0.0.1"
        self.port = 5000

        while True:
            try:
                self.app.run(self.host, self.port, threaded=True)
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    self.port += 1
                    continue
                else:
                    raise
            else:
                break


class Print(InkstitchExtension):
    def build_environment(self):
        if getattr(sys, 'frozen', False):
            template_dir = os.path.join(sys._MEIPASS, "print", "templates")
        else:
            template_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "print", "templates"))

        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            extensions=['jinja2.ext.i18n']
        )

        env.filters['datetimeformat'] = datetimeformat
        env.install_gettext_translations(inkstitch_translation)

        return env

    def strip_namespaces(self, svg):
        # namespace prefixes seem to trip up HTML, so get rid of them
        for element in svg.iter():
            if type(element.tag) == str and element.tag[0] == '{':
                element.tag = element.tag[element.tag.index('}', 1) + 1:]

    def render_svgs(self, stitch_plan, realistic=False):
        svg = deepcopy(self.document).getroot()
        render_stitch_plan(svg, stitch_plan, realistic, visual_commands=False)

        self.strip_namespaces(svg)

        # Now the stitch plan layer will contain a set of groups, each
        # corresponding to a color block.  We'll create a set of SVG files
        # corresponding to each individual color block and a final one
        # for all color blocks together.

        layers = svg.findall("./g[@%s='layer']" % INKSCAPE_GROUPMODE)
        stitch_plan_layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")

        # Make sure there is no leftover translation from stitch plan preview
        stitch_plan_layer.pop('transform')

        # objects outside of the viewbox are invisible
        # TODO: if we want them to be seen, we need to redefine document size to fit the design
        #       this is just a quick fix and doesn't work on realistic view
        svg.set('style', 'overflow:visible;')

        # First, delete all of the other layers.  We don't need them and they'll
        # just bulk up the SVG.
        for layer in layers:
            if layer is not stitch_plan_layer:
                svg.remove(layer)

        overview_svg = etree.tostring(svg).decode('utf-8')
        color_block_groups = stitch_plan_layer.getchildren()
        color_block_svgs = []

        for i, group in enumerate(color_block_groups):
            # clear the stitch plan layer
            del stitch_plan_layer[:]

            # add in just this group
            stitch_plan_layer.append(group)

            # save an SVG preview
            color_block_svgs.append(etree.tostring(svg).decode('utf-8'))

        return overview_svg, color_block_svgs

    def render_html(self, stitch_plan, overview_svg, selected_palette):
        env = self.build_environment()
        template = env.get_template('index.html')

        return template.render(
            view={
                'client_overview': False,
                'client_detailedview': False,
                'operator_overview': True,
                'operator_detailedview': True,
                'custom_page': False
            },
            logo={'src': '', 'title': 'LOGO'},
            date=date.today(),
            client="",
            job={
                'title': '',
                'num_colors': stitch_plan.num_colors,
                'num_color_blocks': len(stitch_plan),
                'num_stops': stitch_plan.num_stops,
                'num_trims': stitch_plan.num_trims,
                'dimensions': stitch_plan.dimensions_mm,
                'num_stitches': stitch_plan.num_stitches,
                'estimated_thread': '',  # TODO
            },
            svg_overview=overview_svg,
            color_blocks=stitch_plan.color_blocks,
            palettes=ThreadCatalog().palette_names(),
            selected_palette=selected_palette,
        )

    def effect(self):
        # It doesn't really make sense to print just a couple of selected
        # objects.  It's almost certain they meant to print the whole design.
        # If they really wanted to print just a few objects, they could set
        # the rest invisible temporarily.
        self.svg.selected.clear()

        if not self.get_elements():
            return

        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches)
        palette = ThreadCatalog().match_and_apply_palette(stitch_plan, self.get_inkstitch_metadata()['thread-palette'])

        overview_svg, color_block_svgs = self.render_svgs(stitch_plan, realistic=False)
        realistic_overview_svg, realistic_color_block_svgs = self.render_svgs(stitch_plan, realistic=True)

        for i, svg in enumerate(color_block_svgs):
            stitch_plan.color_blocks[i].svg_preview = svg

        html = self.render_html(stitch_plan, overview_svg, palette)

        print_server = PrintPreviewServer(
            html=html,
            metadata=self.get_inkstitch_metadata(),
            stitch_plan=stitch_plan,
            realistic_overview_svg=realistic_overview_svg,
            realistic_color_block_svgs=realistic_color_block_svgs
        )
        print_server.start()

        # Wait for print_server.host and print_server.port to be populated.
        # Hacky, but Flask doesn't have an option for a callback to be run
        # after startup.
        time.sleep(0.5)

        browser_window = open_url("http://%s:%s/" % (print_server.host, print_server.port))
        browser_window.wait()
        print_server.stop()
        print_server.join()
