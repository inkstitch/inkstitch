import threading

from ..exceptions import InkstitchException
from ..debug.debug import debug


class ExitThread(InkstitchException):
    """This exception is thrown in a thread to cause it to terminate.

    Presumably we should only catch this at the thread's top level.
    """
    pass


def check_stop_flag() -> None:
    # This getattr() actually looks at the PreviewRenderer instance's stop attribute.
    stop_event: threading.Event | None = getattr(threading.current_thread(), 'stop', None)
    if stop_event is not None and stop_event.is_set():
        debug.log("exiting thread")
        raise ExitThread()
