"""
show_image.py
-------------
Generates an AI image using OpenAI gpt-image-1,
saves it as output.png, and displays it in a popup window.

Install:
    pip3 install openai pillow python-dotenv matplotlib

Run:
    python3 show_image.py
"""

import os
import base64
from io import BytesIO

from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, BadRequestError, APIError
from PIL import Image
import matplotlib.pyplot as plt

# Load OPENAI_API_KEY from .env file
load_dotenv()

PROMPT = (
    "A cute young Bengali girl wearing a traditional saree, with round glasses, "
    "sitting peacefully and reading a book. Cozy indoor environment, "
    "warm lighting, highly detailed, cinematic, realistic, 4k."
)

OUTPUT_FILE = "output.png"


def get_client() -> OpenAI:
    """Build and return an authenticated OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY not found. Add it to your .env file."
        )
    return OpenAI(api_key=api_key)


def generate_image(client: OpenAI, prompt: str) -> Image.Image:
    """Call gpt-image-1 and return a PIL Image object."""
    print("Generating image...")
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="high",
        n=1,
    )
    image_bytes = base64.b64decode(response.data[0].b64_json)
    print("Image received.")
    return Image.open(BytesIO(image_bytes))


def save_image(image: Image.Image, path: str) -> None:
    """Save PIL image to disk."""
    image.save(path)
    print(f"Image saved as: {path}")


def display_image(image: Image.Image, title: str = "Generated Image") -> None:
    """Display image in a matplotlib popup window."""
    print("Displaying image...")
    plt.figure(figsize=(8, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.title(title, fontsize=14, pad=12)
    plt.tight_layout()
    plt.show()  # Blocks until window is closed


def main():
    client = get_client()
    image  = generate_image(client, PROMPT)
    save_image(image, OUTPUT_FILE)
    display_image(image, title="AI Generated Image")
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
