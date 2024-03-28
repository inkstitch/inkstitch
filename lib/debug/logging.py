# Authors: see git history
#
# Copyright (c) 2024 Authors
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
# - inkstitch.debug  - uses in debug module with svg file saving
#
# third-party loggers:
# --------------------
# - werkzeug         - is used by flask
# - shapely.geos     - was used by shapely but currently replaced by exceptions and warnings
#

# --------------------------------------------------------------------------------------------
import os
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib      # built-in in Python 3.11+
else:
    import tomli as tomllib

import warnings          # to control python warnings
import logging           # to configure logging
import logging.config    # to configure logging from dict

from .utils import safe_get     # mimic get method of dict with default value

logger = logging.getLogger('inkstitch')


# --------------------------------------------------------------------------------------------
# activate_logging - configure logging for inkstitch application
def activate_logging(running_as_frozen: bool, ini: dict, SCRIPTDIR: Path):
    if running_as_frozen:                          # in release mode
        activate_for_frozen()
    else:                                          # in development
        activate_for_development(ini, SCRIPTDIR)


# Configure logging in frozen (release) mode of application:
# in release mode normally we want to ignore all warnings and logging, but we can enable it by setting environment variables
#  - INKSTITCH_LOGLEVEL - logging level:
#       'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
#  - PYTHONWARNINGS, -W - warnings action controlled by python
#       actions: 'error', 'ignore', 'always', 'default', 'module', 'once'
def activate_for_frozen():
    loglevel = os.environ.get('INKSTITCH_LOGLEVEL')  # read log level from environment variable or None
    docpath = os.environ.get('DOCUMENT_PATH')  # read document path from environment variable (set by inkscape) or None

    if docpath is not None and loglevel is not None and loglevel.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:

        # The end user enabled logging and warnings are redirected to the input_svg.inkstitch.log file.

        vars = {
            'loglevel': loglevel.upper(),
            'logfilename': Path(docpath).with_suffix('.inkstitch.log')  # log file is created in document path
        }
        config = expand_variables(frozen_config, vars)

        # dictConfig has access to top level variables, dict contains: ext://__main__.var
        #   - restriction: variable must be last token in string - very limited functionality, avoid using it

        # After this operation, logging will be activated, so we can use the logger.
        logging.config.dictConfig(config)  # configure root logger from dict

        logging.captureWarnings(True)                           # capture all warnings to log file with level WARNING
    else:
        logging.disable()                # globally disable all logging of all loggers
        warnings.simplefilter('ignore')  # ignore all warnings


# in development mode we want to use configuration from some LOGGING.toml file
def activate_for_development(ini: dict, SCRIPTDIR: Path):
    logging_config_file = safe_get(ini, "LOGGING", "log_config_file", default=None)
    vars = {'SCRIPTDIR': SCRIPTDIR}        # dynamic data for logging configuration

    if logging_config_file is not None:
        logging_config_file = Path(logging_config_file)
        if logging_config_file.exists():
            with open(logging_config_file, "rb") as f:
                devel_config = tomllib.load(f)   # -> dict
        else:
            raise FileNotFoundError(f"{logging_config_file} file not found")
    else:                                   # if LOGGING.toml file does not exist, use default logging configuration
        vars['loglevel'] = 'DEBUG'          # set log level to DEBUG
        vars['logfilename'] = SCRIPTDIR / "inkstitch.log"  # log file is created in current directory
        devel_config = development_config   # get TOML configuration from module

    configure_logging(devel_config, ini, vars)  # initialize and activate logging configuration

    logger.info("Running in development mode")
    logger.info(f"Using logging configuration from file: {logging_config_file}")
    logger.debug(f"Logging configuration: {devel_config = }")


# --------------------------------------------------------------------------------------------
# configure logging from dictionary:
#  - capture all warnings to log file with level WARNING - depends on warnings_capture
#  - set action for warnings: 'error', 'ignore', 'always', 'default', 'module', 'once' - depends on warnings_action
def configure_logging(config: dict, ini: dict, vars: dict):
    config = expand_variables(config, vars)

    # After this operation, logging will be activated, so we can use the logger.
    logging.config.dictConfig(config)  # configure loggers from dict - using loglevel, logfilename

    warnings_capture = config.get('warnings_capture', True)
    logging.captureWarnings(warnings_capture)  # capture warnings to log file with level WARNING
    warnings_action = config.get('warnings_action', 'default').lower()
    warnings.simplefilter(warnings_action)      # set action for warnings: 'error', 'ignore', 'always', ...

    disable_logging = safe_get(ini, "LOGGING", "disable_logging", default=False)
    if disable_logging:
        logger.warning(f"Logging is disabled by configuration in ini file. {disable_logging = }")
        logging.disable()  # globally disable all logging of all loggers


# Evaluate evaluation of variables in logging configuration:
# "handlers": {
#    "file": {
#         "filename": "%(SCRIPTDIR)s/xxx.log",  # <--- replace %(SCRIPTDIR)s ->  script path
#                     "%(logfilename)s",        # <--- replace %(logfilename)s ->  log file name
#     ...
# "loggers": {
#        "inkstitch": {
#            "level": "%(loglevel)s",           # <--- replace %(loglevel)s ->  log level
#    ...
# - for external configuration file (eg. LOGGING.toml) we cannot pass parameters such as the current directory.
#   - we do: filename = "%(SCRIPTDIR)s/inkstitch.log" -> filename = "path/inkstitch.log"
#   - safety: we can use only predefined variables in myvars, otherwise we get KeyError
# - return modified configuration
# - create logging directory if not exists, directory cannot end with ":" to avoid error with ext:// keys
def expand_variables(cfg: dict, vars: dict):
    for k, v in cfg.get('loggers', {}).items():
        if 'level' in v:                         # replace level in logger
            cfg['loggers'][k]['level'] = v['level'] % vars

    for k, v in cfg.get('handlers', {}).items():
        if 'filename' in v:                      # replace filename in handler
            orig_filename = v['filename']        # original filename for later comparison
            cfg['handlers'][k]['filename'] = v['filename'] % vars
            # create logging directory only if substitution was done, we need to avoid ext:// cfg:// keys
            if orig_filename != cfg['handlers'][k]['filename']:
                dirname = Path(cfg['handlers'][k]['filename']).parent
                if not dirname.exists():
                    # inform user about creating logging directory, otherwise it is silent, logging is not yet active
                    print(f"DEBUG: Creating logging directory: {dirname} ", file=sys.stderr)
                    dirname.mkdir(parents=True, exist_ok=True)
    return cfg


def startup_info(logger: logging.Logger, SCRIPTDIR: Path, running_as_frozen: bool, running_from_inkscape: bool,
                 debug_active: bool, debug_type: str, profiler_type: str):
    logger.info(f"Running as frozen: {running_as_frozen}")
    logger.info(f"Running from inkscape: {running_from_inkscape}")
    logger.info(f"Debugger active: {debug_active}")
    logger.info(f"Debugger type: {debug_type!r}")
    logger.info(f"Profiler type: {profiler_type!r}")

    # log Python version, platform, command line arguments, sys.path
    import sys
    import platform

    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Command line arguments: {sys.argv}")
    logger.debug(f"sys.path: {sys.path}")


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
            "filename": "%(logfilename)s",             # access variable logfilename
            "mode": "w"                                # create new file
        }
    },
    "loggers": {
        "root": {                                      # top level logger
            "level": "%(loglevel)s",                   # access variable loglevel
            "handlers": ["file"],                      # use handler 'file' for logger
        }
    },
}

# ---------------------------------------------------
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
            "filename": "%(logfilename)s",             # ext: --> access variable logfilename
            "mode": "w"                                # create new file
        },
    },
    "loggers": {                                 # configure loggers
        "inkstitch": {                           # specific logger to inkstitch application
            "level": "%(loglevel)s",             # ext: --> access variable loglevel
            "handlers": ["file"],                # use handler 'file' for logger
            "propagate": False,                  # don't propagate to root logger - otherwise all will be logged twice
        },
        "root": {                                # top level logger
            "level": "%(loglevel)s",             # ext: --> access variable loglevel
            "handlers": ["file"],                # use handler 'file' for logger
        }
    },
}
