import subprocess
import sys


def test_simulator_renderer_preloads_wx_submodules():
    # wxWidgets C submodules register the importing thread as the main thread on
    # their first import, so they have to be loaded before the render thread
    # starts. Otherwise wxWidgets rejects timers on the actual main thread.
    code = (
        "import sys; "
        "import lib.gui.simulator.simulator_renderer; "
        "assert 'wx.html' in sys.modules; "
        "assert 'wx.propgrid' in sys.modules"
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
