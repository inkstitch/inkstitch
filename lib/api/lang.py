import os

from flask import Blueprint, jsonify

languages = Blueprint('languages', __name__)


@languages.route('')
def get_lang():
    languages = dict(os.environ)
    return jsonify(languages)
