# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# basic info for inkstitch logging:
# ---------------------------------
# some idea can be found in: Modern Python logging - https://www.youtube.com/watch?v=9L77QExPmI0
#
# logging vs warnings (ChatGPT)
# -----------------------------
# warnings - a built-in mechanism for alerting developers to potential issues or deprecated features within their code.
# logging  - to track events, errors, and other information relevant to the program's operation.
#            Developers typically use logging to understand how their program behaves during execution, diagnose issues,
#            and monitor performance.
#
# Inkstitch is application for Inkscape, so it is not a library, so we use logging for all messages.
#

# root logger:
# ------------
# - The primary logger orchestrates all other loggers through logging.xxx() calls.
# - It should only be utilized at the application's highest level to manage the logging of all loggers.
# - It can easily disable all loggers by invoking logging.disable() and channel all warnings to logging
#   by setting logging.captureWarnings(True) with the level WARNING.
# - The configuration of all loggers can be achieved via a file, and logging.config.dictConfig(logging_dict).


# module logger:
# --------------
#  - Instantiate the logger by invoking logger=getLogger(name).
#      Avoid using __name__ as the name, as it generates numerous loggers per application.
#      The logger name persists globally throughout the application.
#  - Avoid configuring the module logger within the module itself;
#      instead, utilize the top-level application configuration with logging.config.
#      This allows users of the application to customize it according to their requirements.

# example of module logger:
# -------------------------
# import logging
# logger = logging.getLogger('inkstitch')  # create module logger with name 'inkstitch', but configure it at top level of app
# ...
#   logger.debug('debug message')          # example of using module logger
# ...

# top level of the application:
# ----------------------------
# - configure root and other loggers
#   - best practice is to configure from a file: eg logging.config.fileConfig('logging.conf')
#     - consider toml format for logging configuration (json, yaml, xml, dict are also possible)
#

# list of loggers in inkstitch (not complete):
# -------------------------------------------
# - root             - main logger that controls all other loggers
# - inkstitch        - suggested name for inkstitch
# - inkstitch.xyz    - suggested name for inkstitch submodule xyz if needed
#
# third-party loggers:
# --------------------
# - werkzeug         - is used by flask
# - shapely.geos     - was used by shapely but currently replaced by exceptions and warnings
#

# --------------------------------------------------------------------------------------------

import logging
import warnings
from pathlib import Path

from .debug_utils import safe_get # mimic get method of dict with default value

logger = logging.getLogger('inkstitch')

# example of logger configuration for release mode:
# ------------------------------------------------
# - logger suitable for release mode, where we assume that the directory of the input SVG file allows writing the log file.
# - in inkstitch.py we check release mode and environment variable INKSTITCH_LOGLEVEL
#   - this config redirect all loggers to file svg_file.inkstitch.log to directory of svg file
# - set loglevel and logfilename in inkstitch.py before calling logging.config.dictConfig(frozen_config)
frozen_config = {
    "version": 1,    # mandatory key and value (int) is 1
    "disable_existing_loggers": False,  # false enable all loggers not defined here, true disable
    "filters": {},   # no filters
    "formatters": {
        "simple": {  # formatter name (https://docs.python.org/3/library/logging.html#logging.LogRecord)
            "format": '%(asctime)s [%(levelname)s]: %(filename)s.%(funcName)s: %(message)s'  # format string
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",            # type - file output
            "formatter": "simple",                     # use formatter 'simple' for handler 'file'
            "filename": "ext://__main__.logfilename",  # access variable logfilename
            "mode": "w"                                # create new file
        }
    },
    "loggers": {
        "root": {                                      # top level logger
            "level": "ext://__main__.loglevel",        # access variable loglevel
            "handlers": ["file"],                      # use handler 'file' for logger
        }
    },
}

# example of implicit developer logger configuration:
# ---------------------------------------------------
# - configured two loggers: root and inkstitch loggers
# - output is redirected to file 'logfilename' in the directory of inkstitch.py
# - this configuration uses only one log level 'loglevel for both the root and inkstitch loggers.
# - set loglevel and logfilename in inkstitch.py before calling logging.config.dictConfig(development_config)
development_config = {
    "warnings_action": "default",        # dafault action for warnings
    "warnings_capture": True,           # capture warnings to log file with level WARNING

    "version": 1,                       # mandatory key and value (int) is 1
    "disable_existing_loggers": False,  # false enable all loggers not defined here, true disable
    "filters": {},                      # no filters
    "formatters": {
        "simple": {                     # formatter name (https://docs.python.org/3/library/logging.html#logging.LogRecord)
            "format": '%(asctime)s [%(levelname)s]: %(filename)s.%(funcName)s: %(message)s'  # format string
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",            # type - file output
            "formatter": "simple",                     # use formatter 'simple' for handler 'file'
            "filename": "ext://__main__.logfilename",  # ext: --> access variable logfilename
            "mode": "w"                                # create new file
        },
    },
    "loggers": {                                 # configure loggers
        "inkstitch": {                           # specific logger to inkstitch application
            "level": "ext://__main__.loglevel",  # ext: --> access variable loglevel
            "handlers": ["file"],                # use handler 'file' for logger
            "propagate": False,                  # don't propagate to root logger - otherwise all will be logged twice
        },
        "root": {                                # top level logger
            "level": "ext://__main__.loglevel",  # ext: --> access variable loglevel
            "handlers": ["file"],                # use handler 'file' for logger
        }
    },
}


# --------------------------------------------------------------------------------------------
# configure logging from dictionary:
#  - capture all warnings to log file with level WARNING - depends on warnings_capture
#  - set action for warnings: 'error', 'ignore', 'always', 'default', 'module', 'once' - depends on warnings_action
def configure_logging(config:dict, ini:dict, SCRIPTDIR:Path):
    # replace %(SCRIPTDIR)s ->  script path in filenames
    config = evaluate_filenames(config, {'SCRIPTDIR': SCRIPTDIR})
    logging.config.dictConfig(config)  # configure loggers from dict - using loglevel, logfilename

    warnings_capture = config.get('warnings_capture', True)
    logging.captureWarnings(warnings_capture)  # capture warnings to log file with level WARNING
    warnings_action = config.get('warnings_action', 'default').lower()
    warnings.simplefilter(warnings_action)      # set action for warnings: 'error', 'ignore', 'always', ...
    disable_logging = safe_get(ini, "LOGGING", "disable_logging", default=False)
    if disable_logging:
        logger.warning("Logging is disabled by configuration in ini file.")
        logging.disable()  # globally disable all logging of all loggers


# Evaluate filenames in logging configuration using dictionary argument: myvars.
# - for external configuration file (eg. LOGGING.toml) we cannot pass parameters such as the current directory.
#   - we do: filename = "%(SCRIPTDIR)s/inkstitch.log" -> filename = "path/inkstitch.log"
#
# - example of usage:
# "handlers": {
#    "file": {
#         "class": "logging.FileHandler",
#         "filename": "%(SCRIPTDIR)s/xxx.log",  # <--- replace %(SCRIPTDIR)s ->  script path
#    }
# }
#
# returns: logging configuration with evaluated filenames
def evaluate_filenames(cfg: dict, myvars: dict):
    for k, v in cfg.get('handlers', {}).items():
        if 'filename' in v:                      # replace filename in handler
            cfg['handlers'][k]['filename'] = v['filename'] % myvars

            # create logging directory if not exists
            dirname = Path(cfg['handlers'][k]['filename']).parent
            if not dirname.exists():
                dirname.mkdir(parents=True, exist_ok=True)
    return cfg


def startup_info(logger:logging.Logger, SCRIPTDIR:Path, running_as_frozen:bool, running_from_inkscape:bool,
                 debug_active:bool, debug_type:str, profiler_type:str):
    logger.info(f"Running as frozen: {running_as_frozen}")
    logger.info(f"Running from inkscape: {running_from_inkscape}")
    logger.info(f"Debugger active: {debug_active}")
    logger.info(f"Debugger type: {debug_type}")
    logger.info(f"Profiler type: {profiler_type}")

    # log Python version, platform, command line arguments, sys.path
    import sys
    import platform

    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Command line arguments: {sys.argv}")
    logger.info(f"sys.path: {sys.path}")
