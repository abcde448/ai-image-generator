"""
generate_and_display.py
-----------------------
Generates an AI image using OpenAI gpt-image-1 and displays it immediately.

Requirements:
    pip install openai pillow python-dotenv
"""

import os
import base64
from io import BytesIO

from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, BadRequestError, APIError
from PIL import Image

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

load_dotenv()  # Load OPENAI_API_KEY from .env file

PROMPT = (
    "A cute young Bengali girl wearing a traditional saree, with round glasses, "
    "sitting peacefully and reading a book. Cozy indoor environment, warm lighting, "
    "highly detailed, cinematic, realistic, 4k."
)

OUTPUT_FILE = "output.png"

# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------

def main():
    # 1. Validate API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not found. Set it in your .env file.")

    client = OpenAI(api_key=api_key)

    # 2. Generate image
    print("Generating image, please wait...")
    response = client.images.generate(
        model="gpt-image-1",
        prompt=PROMPT,
        size="1024x1024",
        quality="high",
        n=1,
    )

    # 3. Decode base64 image data
    print("Image received. Decoding...")
    image_bytes = base64.b64decode(response.data[0].b64_json)

    # 4. Save to disk
    image = Image.open(BytesIO(image_bytes))
    image.save(OUTPUT_FILE)
    print(f"Image saved as: {OUTPUT_FILE}")

    # 5. Display the image
    print("Displaying image...")
    image.show()  # Opens in default viewer (Preview on macOS)
    print("Done.")


if __name__ == "__main__":
    try:
        main()
    except EnvironmentError as e:
        print(f"[CONFIG ERROR] {e}")
    except AuthenticationError:
        print("[AUTH ERROR] Invalid API key. Check your OPENAI_API_KEY.")
    except RateLimitError:
        print("[RATE LIMIT] Too many requests. Wait and try again.")
    except BadRequestError as e:
        print(f"[BAD REQUEST] {e}")
    except APIError as e:
        print(f"[API ERROR] {e}")
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")
