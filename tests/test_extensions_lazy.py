import subprocess
import sys


def test_importing_output_does_not_import_other_extensions():
    code = (
        "import importlib, sys; "
        "extensions = importlib.import_module('lib.extensions'); "
        "assert 'lib.extensions.print_pdf' not in sys.modules; "
        "assert extensions.Output.__name__ == 'Output'; "
        "assert 'lib.extensions.output' in sys.modules; "
        "assert 'lib.extensions.print_pdf' not in sys.modules; "
        "assert 'lib.threads.catalog' not in sys.modules"
    )
    subprocess.run([sys.executable, "-c", code], check=True)


def test_importing_thread_color_does_not_load_palette_catalog():
    code = (
        "import sys; "
        "from lib.threads import ThreadColor; "
        "assert ThreadColor.__name__ == 'ThreadColor'; "
        "assert 'lib.threads.catalog' not in sys.modules; "
        "assert 'lib.threads.palette' not in sys.modules"
    )
    subprocess.run([sys.executable, "-c", code], check=True)
