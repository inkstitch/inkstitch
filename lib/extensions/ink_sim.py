# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import logging
import os
import shutil
import shlex
import socket
import subprocess
import sys
import tempfile
import time

import inkex

from ..output import write_embroidery_file
from ..stitch_plan import stitch_groups_to_stitch_plan
from .base import InkstitchExtension

INKSIM_IPC_SOCKET = "/tmp/inksim-local"
INKSIM_IPC_TIMEOUT_S = 1.0


class InkSim(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)
        self.logger = logging.getLogger("inkstitch")

    def effect(self):
        if not self.get_elements():
            sys.exit(0)

        start_time = time.time()
        self._log("InkSim: preparing embroidery data...")

        metadata = self.get_inkstitch_metadata()
        collapse_len = metadata['collapse_len_mm']
        min_stitch_len = metadata['min_stitch_len_mm']

        t0 = time.time()
        stitch_groups = self.elements_to_stitch_groups(self.elements)
        self._log(f"InkSim: built {len(stitch_groups)} stitch group(s) in {time.time() - t0:.2f}s")

        t0 = time.time()
        stitch_plan = stitch_groups_to_stitch_plan(stitch_groups, collapse_len=collapse_len, disable_ties=False,
                                                   min_stitch_len=min_stitch_len)
        stitch_count = sum(len(block) for block in stitch_plan)
        self._log(f"InkSim: generated stitch plan ({len(stitch_plan)} block(s), {stitch_count} stitch(es)) in {time.time() - t0:.2f}s")

        # Skip palette matching: inksim only needs the raw RGB colors from the
        # stitch plan.  This saves the time spent loading and scanning thread
        # palettes (~1.5s on a typical design).

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_file_name = temp_file.name

        t0 = time.time()
        write_embroidery_file(temp_file_name, stitch_plan, self.document.getroot())
        self._log(f"InkSim: wrote CSV in {time.time() - t0:.2f}s")

        # Try to reuse a running inksim server; otherwise start a new one.
        # In both cases the temp CSV is deleted by inksim after it has been
        # loaded, so we do not leave temporary files behind.
        if not self._send_to_server(temp_file_name):
            self._run_inksim(temp_file_name)

        self._log(f"InkSim: total time {time.time() - start_time:.2f}s")

        # Prevent inkex from writing the SVG back to stdout; we produced no
        # output that Inkscape should consume.
        sys.exit(0)

    def _log(self, message):
        # Use the Ink/Stitch logger so messages follow the configured logging
        # backend instead of being written to stderr (which Inkscape shows in
        # a modal error dialog).
        self.logger.info(message)

    def _send_to_server(self, csv_path):
        """Ask a running inksim server to open (and delete) the CSV.

        Returns True when the server accepted the command.  A short timeout is
        used so that Inkscape does not freeze when no server is running.
        """
        if not os.path.exists(INKSIM_IPC_SOCKET):
            return False
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.settimeout(INKSIM_IPC_TIMEOUT_S)
                sock.connect(INKSIM_IPC_SOCKET)
                command = {
                    "command": "open_and_delete",
                    "path": csv_path,
                    "focus": True,
                }
                sock.sendall((json.dumps(command) + "\n").encode("utf-8"))
                response = sock.recv(4096).decode("utf-8").strip()
                if response:
                    parsed = json.loads(response)
                    if parsed.get("ok"):
                        self._log(f"InkSim: forwarded {csv_path} to running server")
                        return True
        except (OSError, json.JSONDecodeError) as ex:
            self._log(f"InkSim: server probe failed ({ex})")
        return False

    def _run_inksim(self, csv_path):
        """Launch the external inksim binary in server mode with the CSV.

        The process is started asynchronously so that Inkscape is not blocked
        while inksim is visible.  The binary is resolved in this order:

        1. The ``INKSIM_EXE`` environment variable, if set.
        2. The ``inksim`` executable found on ``PATH``.

        Setting ``INKSIM_EXE`` allows developers to point Ink/Stitch at a local
        inksim checkout without installing it globally.
        """
        ink_sim_env = os.environ.get("INKSIM_EXE")
        if ink_sim_env:
            command = shlex.split(ink_sim_env) + ["--server", "--delete-input", csv_path]
        else:
            ink_sim = shutil.which("inksim")
            if ink_sim is None:
                inkex.errormsg(
                    "inksim not found. Set the INKSIM_EXE environment variable "
                    "or add inksim to PATH."
                )
                sys.exit(1)
            command = [ink_sim, "--server", "--delete-input", csv_path]

        self._log(f"InkSim: launching {' '.join(command)}")
        subprocess.Popen(command,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           start_new_session=True)
