"""
saver.py - Handles saving image bytes to disk with a timestamp filename.
"""

from pathlib import Path
from datetime import datetime

from .logger import get_logger
from . import config

logger = get_logger()


def save_image(image_bytes: bytes) -> Path:
    """
    Persist image bytes to the output directory.

    Filename format: generated_YYYYMMDD_HHMMSS.png

    Args:
        image_bytes: Raw image bytes returned by the generator.

    Returns:
        Absolute Path of the saved file.
    """
    output_dir = Path(config.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = output_dir / f"generated_{timestamp}.{config.IMAGE_FORMAT}"

    filepath.write_bytes(image_bytes)
    logger.info("Image saved → %s", filepath.resolve())

    return filepath
