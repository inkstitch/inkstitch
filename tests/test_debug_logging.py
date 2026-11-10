import logging
from unittest.mock import patch

from lib.debug.logging import configure_logging


def test_configure_logging_limits_colormath2_debug_logs():
    colormath_logger = logging.getLogger("colormath2")
    previous_level = colormath_logger.level
    try:
        with patch("lib.debug.logging.logging.config.dictConfig"), \
                patch("lib.debug.logging.logging.captureWarnings"), \
                patch("lib.debug.logging.warnings.simplefilter"):
            configure_logging({"version": 1, "loggers": {}}, {}, {})

        assert colormath_logger.level == logging.WARNING
    finally:
        colormath_logger.setLevel(previous_level)
