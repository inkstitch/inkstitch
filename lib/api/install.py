import os
import sys
from glob import glob

from flask import Blueprint, jsonify, request

from ..utils import get_bundled_dir, guess_inkscape_config_path

install = Blueprint('install', __name__)


@install.route('/palettes', methods=["POST"])
def palettes():
    try:
        base_path = request.json.get('path') or guess_inkscape_config_path()
        path = os.path.join(base_path, 'palettes')
        src_dir = get_bundled_dir('palettes')
        copy_files(glob(os.path.join(src_dir, "*")), path)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    return jsonify({"status": "success"})


if sys.platform == "win32":
    # If we try to just use shutil.copy it says the operation requires elevation.
    def copy_files(files, dest):
        import winutils

        if not os.path.exists(dest):
            os.makedirs(dest)

        winutils.copy(files, dest)
else:
    def copy_files(files, dest):
        import shutil

        if not os.path.exists(dest):
            os.makedirs(dest)

        for palette_file in files:
            shutil.copy(palette_file, dest)


@install.route('/default-path')
def default_path():
    return guess_inkscape_config_path()
