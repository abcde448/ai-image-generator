"""
main.py - Entry point for the AI Image Generator.

Usage
-----
# Interactive mode (prompts you to type or press Enter for default):
    python main.py

# CLI mode (pass prompt directly):
    python main.py --prompt "A sunset over the Ganges river, oil painting style"

# CLI mode with custom output size/quality (edit config.py or pass env vars):
    python main.py -p "A futuristic Dhaka city skyline at night"
"""

import argparse
import sys
from typing import Optional

import openai

from ai_image_generator.client import build_client
from ai_image_generator.generator import generate_image
from ai_image_generator.saver import save_image
from ai_image_generator.logger import get_logger
from ai_image_generator.config import DEFAULT_PROMPT

logger = get_logger()


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Define and parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate an AI image from a text prompt using OpenAI gpt-image-1.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-p", "--prompt",
        type=str,
        default=None,
        help="Text prompt for image generation. If omitted, you will be asked interactively.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Prompt resolution
# ---------------------------------------------------------------------------

def resolve_prompt(cli_prompt: Optional[str]) -> str:
    """
    Determine the final prompt to use.

    Priority: CLI arg > interactive input > built-in default.

    Args:
        cli_prompt: Value passed via --prompt flag (may be None).

    Returns:
        The prompt string to send to the API.
    """
    if cli_prompt:
        return cli_prompt.strip()

    print("\n--- AI Image Generator ---")
    print(f"Default prompt:\n  {DEFAULT_PROMPT}\n")
    user_input = input("Enter your prompt (or press Enter to use the default): ").strip()

    return user_input if user_input else DEFAULT_PROMPT


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def main() -> None:
    """Orchestrate the full image generation pipeline."""
    args = parse_args()

    try:
        # 1. Resolve prompt
        prompt = resolve_prompt(args.prompt)
        logger.info("Using prompt: %r", prompt[:100])

        # 2. Build authenticated client
        client = build_client()

        # 3. Generate image via OpenAI API
        image_bytes = generate_image(client, prompt)

        # 4. Save to disk
        saved_path = save_image(image_bytes)

        print(f"\n✓ Image generated successfully!")
        print(f"  Saved at: {saved_path.resolve()}\n")

        # Auto-open the image in the default viewer (macOS: Preview)
        import subprocess
        subprocess.run(["open", str(saved_path)], check=False)

    except EnvironmentError as exc:
        logger.error("Setup error: %s", exc)
        sys.exit(1)

    except openai.AuthenticationError:
        logger.error("Authentication failed — check your OPENAI_API_KEY.")
        sys.exit(1)

    except openai.RateLimitError:
        logger.error("Rate limit hit — wait a moment and try again.")
        sys.exit(1)

    except openai.BadRequestError as exc:
        logger.error("Bad request (prompt may violate content policy): %s", exc)
        sys.exit(1)

    except openai.APIError as exc:
        logger.error("OpenAI API error: %s", exc)
        sys.exit(1)

    except ValueError as exc:
        logger.error("Unexpected response from API: %s", exc)
        sys.exit(1)

    except Exception as exc:
        logger.exception("Unhandled error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
