import pyembroidery

from .utils import build_environment, write_inx_file
from .outputs import pyembroidery_output_formats
from ..extensions import extensions, Input, Output


def pyembroidery_debug_formats():
    for format in pyembroidery.supported_formats():
        if 'writer' in format and format['category'] != 'embroidery':
            yield format['extension'], format['description']


def generate_extension_inx_files():
    env = build_environment()

    for extension in extensions:
        if extension is Input or extension is Output:
            continue

        name = extension.name()
        template = env.get_template('%s.inx' % name)
        write_inx_file(name, template.render(formats=pyembroidery_output_formats(),
                                             debug_formats=pyembroidery_debug_formats()))
