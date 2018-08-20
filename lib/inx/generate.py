from .inputs import generate_input_inx_files
from .outputs import generate_output_inx_files
from .extensions import generate_extension_inx_files

def generate_inx_files():
    generate_input_inx_files()
    generate_output_inx_files()
    generate_extension_inx_files()
