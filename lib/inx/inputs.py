import pyembroidery

from .utils import build_environment, write_inx_file


def pyembroidery_input_formats():
    for format in pyembroidery.supported_formats():
        if 'reader' in format and format['category'] == 'embroidery':
            yield format['extension'], format['description']


def generate_input_inx_files():
    env = build_environment()
    template = env.get_template('input.xml')

    for format, description in pyembroidery_input_formats():
        name = "input_%s" % format.upper()
        write_inx_file(name, template.render(format=format, description=description))
