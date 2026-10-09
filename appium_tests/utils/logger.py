"""
DentAI Appium — Logger
========================
Structured logging for the Appium test suite.
Writes to both console and a rotating log file.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

from appium_tests.config.config import LOGS_DIR


def setup_logger(name: str = "dentai_appium") -> logging.Logger:
    """
    Create and configure a named logger.

    Args:
        name: Logger name (use __name__ in callers).

    Returns:
        Configured Logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # ── Formatter ──────────────────────────────────────────────────────────────
    fmt = logging.Formatter(
        fmt="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Console handler ────────────────────────────────────────────────────────
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # ── File handler ───────────────────────────────────────────────────────────
    log_file = LOGS_DIR / f"appium_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    logger.info("Logger initialised → %s", log_file)
    return logger


# Module-level logger for quick imports
log = setup_logger("dentai_appium")
