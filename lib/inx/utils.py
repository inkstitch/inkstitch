import os
from os.path import dirname
from jinja2 import Environment, FileSystemLoader

from ..i18n import translation as inkstitch_translation


_top_path = dirname(dirname(dirname(os.path.realpath(__file__))))
inx_path = os.path.join(_top_path, "inx")
template_path = os.path.join(_top_path, "templates")

def build_environment():
    env = Environment(
        loader = FileSystemLoader(template_path),
        autoescape = True,
        extensions=['jinja2.ext.i18n']
    )

    env.install_gettext_translations(inkstitch_translation)

    return env

def write_inx_file(name, contents):
    inx_file_name = "inkstitch_%s.inx" % name
    with open(os.path.join(inx_path, inx_file_name), 'w') as inx_file:
        print >> inx_file, contents
