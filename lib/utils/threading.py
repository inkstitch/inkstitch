import threading

from ..exceptions import InkstitchException
from ..debug import debug


class ExitThread(InkstitchException):
    """This exception is thrown in a thread to cause it to terminate.

    Presumably we should only catch this at the thread's top level.
    """
    pass


# A default flag used for the main thread.  It will never be set.
_default_stop_flag = threading.Event()


def check_stop_flag():
    # This getattr() actually looks at the PreviewRenderer instance's stop attribute.
    if getattr(threading.current_thread(), 'stop', _default_stop_flag).is_set():
        debug.log("exiting thread")
        raise ExitThread()
