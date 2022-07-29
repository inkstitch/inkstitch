# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from flask import Blueprint, g, jsonify, request

from ..utils.cache import get_stitch_plan_cache
from ..utils.settings import global_settings

preferences = Blueprint('preferences', __name__)


@preferences.route('/', methods=["POST"])
def update_preferences():
    metadata = g.extension.get_inkstitch_metadata()
    metadata.update(request.json['this_svg_settings'])
    global_settings.update(request.json['global_settings'])

    # cache size may have changed
    stitch_plan_cache = get_stitch_plan_cache()
    stitch_plan_cache.size_limit = global_settings['cache_size'] * 1024 * 1024
    stitch_plan_cache.cull()

    return jsonify({"status": "success"})


@preferences.route('/', methods=["GET"])
def get_preferences():
    metadata = g.extension.get_inkstitch_metadata()
    return jsonify({"status": "success",
                    "this_svg_settings": metadata,
                    "global_settings": global_settings
                    })


@preferences.route('/clear_cache', methods=["POST"])
def clear_cache():
    stitch_plan_cache = get_stitch_plan_cache()
    stitch_plan_cache.clear(retry=True)
    return jsonify({"status": "success"})
