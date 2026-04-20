# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import importlib
import os
import sys
from pathlib import Path

SCRIPTDIR = Path(__file__).parent.absolute()

# ---------------------------------------------------------------------------
# Daemon fast-path: delegate to a pre-warmed background process if available.
# Quick check: skip entirely if daemon info file doesn't exist (avoids
# importing json/socket/struct/subprocess on every cold start).
# ---------------------------------------------------------------------------

_daemon_file = os.path.join(str(SCRIPTDIR), '.inkstitch_daemon')

def _daemon_fast_path():
    """Try to delegate to the Ink/Stitch daemon.  Returns silently on failure."""
    import json
    import socket
    import struct
    import subprocess

    if len(sys.argv) < 2:
        return  # no args — fall through to normal error handling below

    # Quick-parse --extension from argv (avoid importing argparse logic)
    ext_name = None
    remaining = []
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg.startswith('--extension='):
            ext_name = arg.split('=', 1)[1]
        elif arg == '--extension':
            if i + 1 < len(sys.argv):
                i += 1
                ext_name = sys.argv[i]
        else:
            remaining.append(arg)
        i += 1

    if not ext_name:
        return

    scriptdir = str(SCRIPTDIR)
    daemon_file = os.path.join(scriptdir, '.inkstitch_daemon')

    # --- helper: start daemon in background for *next* invocation ----------
    def _start_daemon():
        daemon_script = os.path.join(scriptdir, 'inkstitch_daemon.py')
        if not os.path.exists(daemon_script):
            return
        try:
            log_file = open(os.path.join(scriptdir, '.daemon.log'), 'a')
            if sys.platform == 'win32':
                subprocess.Popen(
                    [sys.executable, daemon_script],
                    close_fds=True, stdout=subprocess.DEVNULL, stderr=log_file,
                    creationflags=0x08000000 | 0x00000008)  # CREATE_NO_WINDOW | DETACHED_PROCESS
            else:
                subprocess.Popen(
                    [sys.executable, daemon_script],
                    close_fds=True, stdout=subprocess.DEVNULL, stderr=log_file,
                    start_new_session=True)
        except Exception:
            pass

    # --- try to read daemon info -------------------------------------------
    if not os.path.exists(daemon_file):
        _start_daemon()
        return

    try:
        with open(daemon_file) as f:
            info = json.load(f)
        port = int(info['port'])
    except (json.JSONDecodeError, KeyError, ValueError, OSError):
        _start_daemon()
        return

    # --- read stdin (SVG for effect extensions, empty for input) -----------
    stdin_data = b''
    try:
        if not sys.stdin.isatty():
            stdin_data = sys.stdin.buffer.read()
    except Exception:
        pass

    # --- connect and send request ------------------------------------------
    def _recv(sock, n):
        buf = bytearray()
        while len(buf) < n:
            c = sock.recv(min(n - len(buf), 131072))
            if not c:
                raise ConnectionError()
            buf.extend(c)
        return bytes(buf)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(600)  # extensions can take time (GUI interaction)
        sock.connect(('127.0.0.1', port))

        # Send header
        hdr = json.dumps({
            'command': 'run',
            'extension': ext_name,
            'args': remaining,
        }).encode('utf-8')
        sock.sendall(struct.pack('!I', len(hdr)) + hdr)

        # Send stdin data
        sock.sendall(struct.pack('!I', len(stdin_data)) + stdin_data)

        # Receive response header
        resp_len = struct.unpack('!I', _recv(sock, 4))[0]
        resp = json.loads(_recv(sock, resp_len))


        # Receive stdout
        out_len = struct.unpack('!I', _recv(sock, 4))[0]
        out_data = _recv(sock, out_len) if out_len else b''

        # Receive stderr
        err_len = struct.unpack('!I', _recv(sock, 4))[0]
        err_data = _recv(sock, err_len) if err_len else b''

        sock.close()

        # Write to real stdout/stderr
        try:
            if out_data and sys.stdout and hasattr(sys.stdout, 'buffer'):
                sys.stdout.buffer.write(out_data)
                sys.stdout.buffer.flush()
            if err_data and sys.stderr and hasattr(sys.stderr, 'buffer'):
                sys.stderr.buffer.write(err_data)
                sys.stderr.buffer.flush()
        except Exception:
            pass

        sys.exit(resp.get('exit_code', 0))

    except (ConnectionRefusedError, ConnectionResetError, ConnectionError,
            socket.timeout, OSError):
        # Daemon unreachable — fall through to normal execution
        _start_daemon()
        return

# Try the fast path (exits on success, returns on failure)
if os.path.exists(_daemon_file):
    _daemon_fast_path()

# ---------------------------------------------------------------------------
# Normal (cold) path — reached only when daemon is unavailable
# ---------------------------------------------------------------------------

running_as_frozen = getattr(sys, 'frozen', None) is not None

if len(sys.argv) < 2:
    msg = "No arguments given, exiting!\n\nInk/Stitch is an Inkscape extension.\n\nPlease enter arguments or run Ink/Stitch through the Inkscape extensions menu."
    if running_as_frozen:
        try:
            import wx
            app = wx.App()
            dlg = wx.MessageDialog(None, msg, "Inkstitch", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        except ImportError:
            print(msg, file=sys.stderr)
    else:
        print(msg, file=sys.stderr)
    sys.exit(1)

# --- Fast path: skip heavy debug imports when no DEBUG.toml exists ---
debug_toml = SCRIPTDIR / "DEBUG.toml"
_has_debug_toml = debug_toml.exists()

if _has_debug_toml or running_as_frozen:
    # Full debug/logging setup (original path)
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib

    import logging
    import lib.debug.utils as debug_utils
    import lib.debug.logging as debug_logging
    from lib.debug.utils import safe_get

    old_debug_ini = SCRIPTDIR / "DEBUG.ini"
    if old_debug_ini.exists():
        print("ERROR: old DEBUG.ini exists, please reformat it to DEBUG.toml and remove DEBUG.ini file", file=sys.stderr)
        sys.exit(1)

    if _has_debug_toml:
        with debug_toml.open("rb") as f:
            ini: dict = tomllib.load(f)
    else:
        ini = {}

    if not running_as_frozen and safe_get(ini, "DEBUG", "force_frozen", default=False):
        running_as_frozen = True

    debug_logging.activate_logging(running_as_frozen, ini, SCRIPTDIR)

    running_from_inkscape = os.environ.get('INKSTITCH_OFFLINE_SCRIPT', '').lower() not in ('true', '1', 'yes', 'y')

    debug_active = bool((gettrace := getattr(sys, 'gettrace')) and gettrace())
    debug_type = 'none'
    profiler_type = 'none'

    if not running_as_frozen:
        if not debug_active:
            debug_type = str(debug_utils.resolve_debug_type(ini))
        profiler_type = str(debug_utils.resolve_profiler_type(ini))
        if running_from_inkscape:
            if safe_get(ini, "DEBUG", "create_bash_script", default=False):
                debug_utils.write_offline_debug_script(SCRIPTDIR, ini)
            if safe_get(ini, "DEBUG", "disable_from_inkscape", default=False):
                debug_type = 'none'
        prefer_pip_inkex = safe_get(ini, "LIBRARY", "prefer_pip_inkex", default=True)
        if prefer_pip_inkex and 'PYTHONPATH' in os.environ:
            debug_utils.reorder_sys_path()

    if debug_type != 'none':
        from lib.debug.debugger import init_debugger
        init_debugger(debug_type, ini)
        debug_active = bool((gettrace := getattr(sys, 'gettrace')) and gettrace())

    from lib.debug.debug import debug
    debug.enable()

    logger = logging.getLogger("inkstitch")
    debug_logging.startup_info(logger, SCRIPTDIR, running_as_frozen, running_from_inkscape, debug_active, debug_type, profiler_type)

    if running_as_frozen and not debug_logging.frozen_debug_active():
        debug_logging.disable_warnings()

else:
    # Fast path: no DEBUG.toml, not frozen — skip all debug imports
    # Just do sys.path reorder for pip inkex preference
    if 'PYTHONPATH' in os.environ:
        _pp = os.environ['PYTHONPATH'].split(os.pathsep)
        sys.path = [p for p in sys.path if p not in _pp]
        _pp = [p for p in _pp if not p.endswith('deprecated-simple') and os.path.exists(p)]
        sys.path.extend(_pp)

    debug_active = bool((gettrace := getattr(sys, 'gettrace')) and gettrace())
    debug_type: str = 'none'
    profiler_type: str = 'none'
    ini: dict = {}


# Quick-parse --extension from argv (no argparse import needed)
extension_name = None
remaining_args = []
_i = 1
while _i < len(sys.argv):
    _a = sys.argv[_i]
    if _a.startswith('--extension='):
        extension_name = _a.split('=', 1)[1]
    elif _a == '--extension':
        _i += 1
        if _i < len(sys.argv):
            extension_name = sys.argv[_i]
    else:
        remaining_args.append(_a)
    _i += 1

if extension_name is None:
    print("Error: no --extension argument provided", file=sys.stderr)
    sys.exit(1)

# example: foo_bar_baz -> FooBarBaz
extension_class_name = extension_name.title().replace("_", "")

# --- Ultra-fast path for Input extension (lxml + pystitch only, no inkex) ---
if extension_class_name == 'Input' and not debug_active and profiler_type == 'none' and remaining_args:
    _fast_input_ok = False
    try:
        from lib.extensions.input_fast import run_fast_input
        # Suppress stderr (GTK spam)
        _stderr_dup = os.dup(2)
        with open(os.devnull, 'w') as _devnull:
            os.dup2(_devnull.fileno(), 2)
        try:
            run_fast_input(remaining_args[0])
            _fast_input_ok = True
        except SystemExit as _se:
            # Propagate normal exit (e.g. sys.exit(0) from color-format check)
            os.dup2(_stderr_dup, 2)
            sys.exit(_se.code)
        except Exception:
            os.dup2(_stderr_dup, 2)
        else:
            os.dup2(_stderr_dup, 2)
    except ImportError:
        pass
    if _fast_input_ok:
        sys.exit(0)

# --- Ultra-fast path for Output extension (lxml + pystitch only, no inkex) ---
if extension_class_name == 'Output' and not debug_active and profiler_type == 'none':
    # Parse --format and other settings from remaining_args
    _fmt = None
    _output_settings = {}
    for _arg in remaining_args:
        if _arg.startswith('--') and not _arg.startswith('--id='):
            _kv = _arg[2:].split('=', 1)
            if len(_kv) == 2:
                _k, _v = _kv
                if _k == 'format':
                    _fmt = _v
                else:
                    try:
                        _v = float(_v)
                    except ValueError:
                        _v = {'true': True, 'false': False}.get(_v, _v)
                    _output_settings[_k] = _v

    # Find the SVG file path (last non-option argument)
    _svg_file = None
    for _arg in remaining_args:
        if not _arg.startswith('--'):
            _svg_file = _arg

    if _fmt and _svg_file and os.path.isfile(_svg_file):
        try:
            with open(_svg_file, 'rb') as _f:
                _svg_buf = _f.read()
        except Exception:
            _svg_buf = b''

        try:
            from lib.extensions.output_fast import run_fast_output
            _stderr_dup2 = os.dup(2)
            with open(os.devnull, 'w') as _devnull:
                os.dup2(_devnull.fileno(), 2)
            try:
                if run_fast_output(_fmt, _output_settings, _svg_buf):
                    os.dup2(_stderr_dup2, 2)
                    sys.exit(0)
            except Exception:
                pass
            os.dup2(_stderr_dup2, 2)
        except ImportError:
            pass
        del _svg_buf

# Lazy-import only the extension class we need (not all 80+ extensions)
extensions = importlib.import_module('lib.extensions')
extension_class = getattr(extensions, extension_class_name)
extension = extension_class()

# extension run(), we differentiate between debug and normal mode
# - in debug or profile mode we debug or profile extension.run() method
# - in normal mode we run extension.run() in try/except block to catch all exceptions and hide GTK spam
if debug_active or profiler_type != "none":  # if debug or profile mode
    if profiler_type == 'none':             # only debugging
        extension.run(args=remaining_args)
    else:                                  # do profiling
        import lib.debug.utils as debug_utils
        debug_utils.profile(profiler_type, SCRIPTDIR, ini, extension, remaining_args)

else:   # if not debug nor profile mode
    # Inline stderr suppression (avoids importing lib.utils.io before run)
    _stderr_dup = os.dup(2)
    with open(os.devnull, 'w') as _devnull:
        os.dup2(_devnull.fileno(), 2)

    exception = None
    try:
        extension.run(args=remaining_args)
    except (SystemExit, KeyboardInterrupt):
        os.dup2(_stderr_dup, 2)
        raise
    except Exception as exc:
        # Lazy-import error handling only when an error actually occurs
        os.dup2(_stderr_dup, 2)
        from lxml.etree import XMLSyntaxError
        from inkex.utils import errormsg
        from lib.i18n import _
        from lib.exceptions import InkstitchException, format_uncaught_exception

        if isinstance(exc, XMLSyntaxError):
            msg = _("Ink/Stitch cannot read your SVG file. "
                    "This is often the case when you use a file which has been created with Adobe Illustrator.")
            msg += "\n\n"
            msg += _("Try to import the file into Inkscape through 'File > Import...' (Ctrl+I)")
            errormsg(msg)
        elif isinstance(exc, InkstitchException):
            errormsg(str(exc))
        else:
            errormsg(format_uncaught_exception())
            sys.exit(1)
    else:
        # Restore stderr on success
        os.dup2(_stderr_dup, 2)

    sys.exit(0)
