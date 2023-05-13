# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import errno
import logging
import socket
import sys
import time
from threading import Thread
from contextlib import closing

import requests
from flask import Flask, g
from werkzeug.serving import make_server

from ..utils.json import InkStitchJSONProvider
from .simulator import simulator
from .stitch_plan import stitch_plan
from .preferences import preferences
from .page_specs import page_specs
from .lang import languages
# this for electron axios
from flask_cors import CORS


class APIServer(Thread):
    def __init__(self, *args, **kwargs):
        self.extension = args[0]
        Thread.__init__(self, *args[1:], **kwargs)
        self.daemon = True
        self.app = None
        self.host = None
        self.port = None
        self.ready = False

        self.__setup_app()
        self.flask_server = None
        self.server_thread = None

    def __setup_app(self):  # noqa: C901
        # Disable warning about using a development server in a production environment
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None

        self.app = Flask(__name__)
        CORS(self.app)
        self.app.json = InkStitchJSONProvider(self.app)

        self.app.register_blueprint(simulator, url_prefix="/simulator")
        self.app.register_blueprint(stitch_plan, url_prefix="/stitch_plan")
        self.app.register_blueprint(preferences, url_prefix="/preferences")
        self.app.register_blueprint(page_specs, url_prefix="/page_specs")
        self.app.register_blueprint(languages, url_prefix="/languages")

        @self.app.before_request
        def store_extension():
            # make the InkstitchExtension object available to the view handling
            # this request
            g.extension = self.extension

        @self.app.route('/ping')
        def ping():
            return "pong"

    def stop(self):
        self.flask_server.shutdown()
        self.server_thread.join()

    def disable_logging(self):
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

    # https://github.com/aluo-x/Learning_Neural_Acoustic_Fields/blob/master/train.py
    # https://github.com/pytorch/pytorch/issues/71029
    def find_free_port(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('localhost', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def run(self):
        self.disable_logging()

        self.host = "127.0.0.1"
        self.port = self.find_free_port()
        self.flask_server = make_server(self.host, self.port, self.app)
        self.server_thread = Thread(target=self.flask_server.serve_forever)
        self.server_thread.start()

    def ready_checker(self):
        """Wait until the server is started.

        Annoyingly, there's no way to get a callback to be run when the Flask
        server starts.  Instead, we'll have to poll.
        """

        while True:
            if self.port:
                try:
                    response = requests.get("http://%s:%s/ping" % (self.host, self.port))
                    if response.status_code == 200:
                        break
                except socket.error as e:
                    if e.errno == errno.ECONNREFUSED:
                        pass
                    else:
                        raise

            time.sleep(0.1)

    def start_server(self):
        """Start the API server.

        returns: port (int) -- the port that the server is listening on
                   (on localhost)
        """

        checker = Thread(target=self.ready_checker)
        checker.start()
        self.start()
        checker.join()

        return self.port
