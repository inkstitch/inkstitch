import errno
import logging
import socket
from threading import Thread
import time

from flask import Flask, request, g
import requests

from .simulator import simulator


class APIServer(Thread):
    def __init__(self, *args, **kwargs):
        self.extension = args[0]
        Thread.__init__(self, *args[1:], **kwargs)
        self.daemon = True
        self.shutting_down = False
        self.app = None
        self.host = None
        self.port = None
        self.ready = False

        self.__setup_app()

    def __setup_app(self):  # noqa: C901
        self.app = Flask(__name__)

        self.app.register_blueprint(simulator, url_prefix="/simulator")

        @self.app.before_request
        def store_extension():
            # make the InkstitchExtension object available to the view handling
            # this request
            g.extension = self.extension

        @self.app.route('/shutdown', methods=['POST'])
        def shutdown():
            self.shutting_down = True
            request.environ.get('werkzeug.server.shutdown')()
            return "shutting down"

        @self.app.route('/ping')
        def ping():
            return "pong"

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
                except socket.error, e:
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
