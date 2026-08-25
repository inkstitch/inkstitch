# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import shutil
import subprocess
import sys
import tempfile
import time

import inkex

from ..output import write_embroidery_file
from ..stitch_plan import stitch_groups_to_stitch_plan
from .base import InkstitchExtension


class InkSim(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)

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

        # Launch inksim asynchronously so that Inkscape does not freeze while
        # the external viewer/editor is open.  The temp CSV is left on disk so
        # inksim has time to read it.
        self._run_inksim(temp_file_name)

        self._log(f"InkSim: total time {time.time() - start_time:.2f}s")

        # Prevent inkex from writing the SVG back to stdout; we produced no
        # output that Inkscape should consume.
        sys.exit(0)

    def _log(self, message):
        # Messages are printed to stderr because Inkscape captures stdout for
        # extension output.  With show-stderr="true" in the INX file these
        # messages are visible to the user in the Inkscape error dialog.
        print(message, file=sys.stderr, flush=True)

    def _run_inksim(self, csv_path):
        """Launch the external inksim binary with the generated CSV.

        The process is started asynchronously so that Inkscape is not blocked
        while inksim is visible.  The binary is expected to be available on
        PATH.  If it is not, users can place it on PATH or symlink it into a
        standard location.
        """
        ink_sim = shutil.which("inksim")
        if ink_sim is None:
            inkex.errormsg("inksim not found on PATH. Please install inksim or add it to PATH.")
            sys.exit(1)

        self._log(f"InkSim: launching {ink_sim} {csv_path}")
        subprocess.Popen([ink_sim, csv_path],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           start_new_session=True)
