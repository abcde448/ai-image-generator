"""
stable_diffusion_generate.py
-----------------------------
Generates an AI image using Stable Diffusion (no API key needed).
Uses the diffusers library from Hugging Face.

Install:
    pip3 install diffusers transformers accelerate torch pillow matplotlib

Run:
    python3 stable_diffusion_generate.py

Note:
    First run downloads the model (~4GB). Subsequent runs use the cache.
    Works on CPU (slow ~5-10 min) or MPS/GPU (fast ~10-30 sec).
"""

import torch
import matplotlib.pyplot as plt
from diffusers import StableDiffusionPipeline
from PIL import Image

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROMPT = (
    "A cute young Bengali girl wearing a saree, with round glasses, "
    "reading a book in a cozy room with warm lighting, "
    "highly detailed, cinematic"
)

NEGATIVE_PROMPT = (
    "blurry, low quality, distorted, deformed, ugly, bad anatomy"
)

MODEL_ID   = "runwayml/stable-diffusion-v1-5"  # free, no login required
OUTPUT_FILE = "output.png"


# ---------------------------------------------------------------------------
# Device detection (MPS for Apple Silicon, CUDA for Nvidia, else CPU)
# ---------------------------------------------------------------------------

def get_device() -> str:
    if torch.backends.mps.is_available():
        return "mps"          # Apple Silicon (M1/M2/M3)
    elif torch.cuda.is_available():
        return "cuda"         # Nvidia GPU
    else:
        return "cpu"          # Fallback (slow but works)


# ---------------------------------------------------------------------------
# Pipeline loader
# ---------------------------------------------------------------------------

def load_pipeline(device: str) -> StableDiffusionPipeline:
    """Download (first run) or load from cache and move to device."""
    print(f"Loading Stable Diffusion model on: {device.upper()}")
    print("(First run downloads ~4GB — this may take a few minutes...)\n")

    # float16 causes black images on MPS (Apple Silicon) — use float32 always
    dtype = torch.float16 if device == "cuda" else torch.float32

    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        safety_checker=None,       # disable NSFW filter for speed
        requires_safety_checker=False,
    )
    pipe = pipe.to(device)

    # Memory optimisation for MPS / CPU
    if device != "cuda":
        pipe.enable_attention_slicing()

    return pipe


# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

def generate_image(pipe: StableDiffusionPipeline) -> Image.Image:
    """Run inference and return a PIL Image."""
    print("Generating image...")
    result = pipe(
        prompt=PROMPT,
        negative_prompt=NEGATIVE_PROMPT,
        num_inference_steps=30,   # higher = better quality, slower
        guidance_scale=7.5,       # how closely to follow the prompt
        width=512,
        height=512,
    )
    print("Image generated.")
    return result.images[0]


# ---------------------------------------------------------------------------
# Save & display
# ---------------------------------------------------------------------------

def save_image(image: Image.Image, path: str) -> None:
    image.save(path)
    print(f"Image saved as: {path}")


def display_image(image: Image.Image) -> None:
    print("Displaying image...")
    plt.figure(figsize=(7, 7))
    plt.imshow(image)
    plt.axis("off")
    plt.title("Stable Diffusion — Generated Image", fontsize=13, pad=10)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    device = get_device()
    pipe   = load_pipeline(device)
    image  = generate_image(pipe)
    save_image(image, OUTPUT_FILE)
    display_image(image)
    print("Done.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled by user.")
    except Exception as e:
        print(f"[ERROR] {e}")
        raise
