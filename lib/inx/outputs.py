import pyembroidery

from .utils import build_environment, write_inx_file


def pyembroidery_output_formats():
    for format in pyembroidery.supported_formats():
        if 'writer' in format:
            description = format['description']
            if format['category'] != "embroidery":
                description = "%s [DEBUG]" % description
            yield format['extension'], description, format['mimetype'], format['category']


def generate_output_inx_files():
    env = build_environment()
    template = env.get_template('output.xml')

    for format, description, mimetype, category in pyembroidery_output_formats():
        name = "output_%s" % format.upper()
        write_inx_file(name, template.render(format=format, mimetype=mimetype, description=description))
