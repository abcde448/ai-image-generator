"""
generator.py - Image generation logic.
Calls the OpenAI API and returns raw image bytes.
"""

import base64
import openai

from .logger import get_logger
from . import config

logger = get_logger()


def generate_image(client: openai.OpenAI, prompt: str) -> bytes:
    """
    Generate an image for the given prompt using gpt-image-1.

    Args:
        client: Authenticated OpenAI client.
        prompt: Text description of the desired image.

    Returns:
        Raw PNG/JPEG bytes of the generated image.

    Raises:
        ValueError: If the API returns no image data.
        openai.OpenAIError: On any API-level failure.
    """
    logger.info("Generating image for prompt: %r", prompt[:80])
    logger.info("Model: %s | Size: %s | Quality: %s",
                config.MODEL, config.IMAGE_SIZE, config.IMAGE_QUALITY)

    response = client.images.generate(
        model=config.MODEL,
        prompt=prompt,
        size=config.IMAGE_SIZE,
        quality=config.IMAGE_QUALITY,
        n=1,
    )

    b64_data = response.data[0].b64_json
    if not b64_data:
        raise ValueError("API returned an empty image payload.")

    logger.info("Image received from API — decoding...")
    return base64.b64decode(b64_data)
