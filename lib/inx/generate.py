from .about import generate_about_inx_file
from .extensions import generate_extension_inx_files
from .inputs import generate_input_inx_files
from .outputs import generate_output_inx_files
from .utils import iterate_inx_locales


def generate_inx_files():
    for locale in iterate_inx_locales():
        generate_input_inx_files()
        generate_output_inx_files()
        generate_extension_inx_files()
        generate_about_inx_file()
