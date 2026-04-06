"""
client.py - OpenAI client initialisation.
Reads the API key from the environment / .env file.
"""

import os
import openai
from dotenv import load_dotenv

from .logger import get_logger

logger = get_logger()


def build_client() -> openai.OpenAI:
    """
    Load credentials and return an authenticated OpenAI client.

    Raises:
        EnvironmentError: If OPENAI_API_KEY is missing.
    """
    load_dotenv()  # picks up .env if present

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY not found. "
            "Set it in your environment or create a .env file."
        )

    logger.info("OpenAI client initialised successfully.")
    return openai.OpenAI(api_key=api_key)
