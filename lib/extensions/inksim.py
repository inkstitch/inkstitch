# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import logging
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import inkex
import wx

from ..output import write_embroidery_file
from ..stitch_plan import stitch_groups_to_stitch_plan
from .base import InkstitchExtension


def _resolve_document_path():
    """Return the Inkscape document path or the current working directory."""
    document_path = os.environ.get("DOCUMENT_PATH")
    if document_path:
        return document_path
    return str(Path.cwd())


class Inksim(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)
        self.logger = logging.getLogger("inkstitch")
        self._play = True

    def effect(self):
        if not self.get_elements():
            sys.exit(0)

        # Show a lightweight progress dialog so the user sees something is
        # happening while we build the stitch plan and launch inksim.
        app = wx.App()
        progress = wx.ProgressDialog(
            "InkSim",
            "Preparing embroidery data...",
            maximum=100,
            parent=None,
            style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_SMOOTH,
        )
        progress.CenterOnScreen()
        progress.Pulse()

        start_time = time.time()
        self._log("InkSim: preparing embroidery data...")

        try:
            metadata = self.get_inkstitch_metadata()
            collapse_len = metadata['collapse_len_mm']
            min_stitch_len = metadata['min_stitch_len_mm']

            progress.Update(10, "Building stitch groups...")
            t0 = time.time()
            stitch_groups = self.elements_to_stitch_groups(self.elements)
            self._log(f"InkSim: built {len(stitch_groups)} stitch group(s) in {time.time() - t0:.2f}s")

            progress.Update(40, "Generating stitch plan...")
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

            progress.Update(70, "Writing CSV file...")
            t0 = time.time()
            write_embroidery_file(temp_file_name, stitch_plan, self.document.getroot())
            self._log(f"InkSim: wrote CSV in {time.time() - t0:.2f}s")

            # Try to reuse a running inksim server; otherwise start a new one.
            # In both cases the temp CSV is deleted by inksim after it has been
            # loaded, so we do not leave temporary files behind.
            progress.Update(90, "Starting InkSim simulator...")
            server_running = self._send_to_server(temp_file_name)
            if not server_running:
                self._run_inksim(temp_file_name)

            self._log(f"InkSim: total time {time.time() - start_time:.2f}s")
        finally:
            progress.Destroy()
            app.Destroy()

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

        Returns True when the server accepted the command.  The request is sent
        by invoking ``inksim --send-command`` so that Ink/Stitch does not need
        to know the platform-specific IPC transport used by Qt (named pipes on
        Windows, local sockets on Unix).
        """
        ink_sim_env = os.environ.get("INKSIM_EXE")
        if ink_sim_env:
            base_command = shlex.split(ink_sim_env)
        else:
            ink_sim = shutil.which("inksim")
            if ink_sim is None:
                return False
            base_command = [ink_sim]

        command_payload = {
            "command": "open_and_delete",
            "path": csv_path,
            "focus": True,
            "autoplay": True,
            "document_path": _resolve_document_path(),
        }
        command = base_command + [
            "--send-command",
            json.dumps(command_payload),
        ]
        self._log(f"InkSim: forwarding to server with {' '.join(command)}")
        kwargs = {}
        if sys.platform == "win32":
            # Avoid creating a console window on Windows when running the
            # packaged inksim binary.
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=3,
                **kwargs,
            )
        except (OSError, subprocess.TimeoutExpired) as ex:
            self._log(f"InkSim: server probe failed ({ex})")
            return False

        stdout = result.stdout.decode("utf-8", errors="replace").strip()
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        self._log(
            f"InkSim: server probe exited {result.returncode}; "
            f"stdout={stdout!r}; stderr={stderr!r}"
        )

        if result.returncode != 0:
            # No server running or command rejected; the stderr usually
            # contains a brief message which we keep in the log only.
            return False

        try:
            response = json.loads(stdout)
        except json.JSONDecodeError:
            return False

        if response.get("ok"):
            self._log("InkSim: forwarded CSV to running server")
            return True
        return False

    def _run_inksim(self, csv_path):
        """Launch the external inksim binary in server mode with the CSV.

        The process is started asynchronously so that Inkscape is not blocked
        while inksim is visible.  The binary is resolved in this order:

        1. The ``INKSIM_EXE`` environment variable, if set.
        2. The Windows ``inksim-gui`` executable, or ``inksim`` on other
           platforms, found on ``PATH``.

        Setting ``INKSIM_EXE`` allows developers to point Ink/Stitch at a local
        inksim checkout without installing it globally.
        """
        ink_sim_env = os.environ.get("INKSIM_EXE")
        if ink_sim_env:
            command = shlex.split(ink_sim_env)
        else:
            launcher = "inksim-gui" if sys.platform == "win32" else "inksim"
            ink_sim = shutil.which(launcher)
            if ink_sim is None:
                inkex.errormsg(
                    f"{launcher} not found. Set the INKSIM_EXE environment variable "
                    f"or add {launcher} to PATH."
                )
                sys.exit(1)
            command = [ink_sim]

        command += ["--server", "--delete-input"]
        if self._play:
            command.append("--play")
        command += ["--document-path", _resolve_document_path()]
        command.append(csv_path)

        self._log(f"InkSim: launching {' '.join(command)}")
        kwargs = {"start_new_session": True}
        if sys.platform == "win32":
            # Avoid creating a console window on Windows when running the
            # packaged inksim binary.
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        subprocess.Popen(command,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         **kwargs)

