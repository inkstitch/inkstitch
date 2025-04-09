import threading
import sys
from lib.i18n import _
from functools import wraps
import wx

def with_cancel_dialog(title: str, message: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # A hack: the app must be kept alive or there's a segfault in wxwidgets when it's deallocated
            # So we'll keep it around in the global scope. This is somwehat bad, but it's only ever
            # set in `wrapper`, which is only called when a "with_cancel_dialog" function is called.
            global app
            app = wx.App()

            dialog = wx.ProgressDialog(_(title), _(message), maximum=1, style=wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT)

            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()

            while True:
                ok, abort = dialog.Pulse()
                if not ok:
                    sys.exit(1)

                thread.join(0.1)
                if not thread.is_alive():
                    break

            dialog.Destroy()
        
        return wrapper

    return decorator
