import pyembroidery

from .utils import build_environment, write_inx_file


def pyembroidery_output_formats():
    for format in pyembroidery.supported_formats():
        if 'writer' in format and format['category'] == 'embroidery':
            yield format['extension'], format['description']


def generate_output_inx_files():
    env = build_environment()
    template = env.get_template('output.inx')

    for format, description in pyembroidery_output_formats():
        name = "output_%s" % format.upper()
        mimetype="application/x-embroidery-%s" % format
        write_inx_file(name, template.render(format=format, mimetype=mimetype, description=description))

    write_inx_file('output_csv', template.render(format='csv', mimetype='text/csv', description="DEBUG"))
