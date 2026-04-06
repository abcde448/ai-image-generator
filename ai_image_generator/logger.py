"""
logger.py - Shared logger instance for the entire project.
"""

import logging


def get_logger(name: str = "ai_image_gen") -> logging.Logger:
    """Return a configured logger."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s  [%(levelname)-8s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
