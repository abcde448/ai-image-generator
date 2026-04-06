"""
app.py - Streamlit AI Image Generator (Stable Diffusion, runs locally)
-----------------------------------------------------------------------
Install:
    pip3 install streamlit diffusers transformers accelerate torch pillow

Run:
    python3 -m streamlit run app.py

No API key required. Model downloads ~4GB on first run.
"""

import torch
import streamlit as st
from diffusers import StableDiffusionPipeline
from PIL import Image

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODEL_ID    = "runwayml/stable-diffusion-v1-5"
OUTPUT_FILE = "output.png"

# ---------------------------------------------------------------------------
# Device detection
# ---------------------------------------------------------------------------

def get_device() -> str:
    if torch.backends.mps.is_available():
        return "mps"    # Apple Silicon M1/M2/M3
    elif torch.cuda.is_available():
        return "cuda"   # Nvidia GPU
    return "cpu"

# ---------------------------------------------------------------------------
# Pipeline — cached so it loads only once per session
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner="Loading Stable Diffusion model (first run ~4GB)...")
def load_pipeline() -> StableDiffusionPipeline:
    device = get_device()
    # float16 causes black images on MPS — use float32 for MPS and CPU
    dtype  = torch.float16 if device == "cuda" else torch.float32

    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        safety_checker=None,
        requires_safety_checker=False,
    )
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()  # reduces memory usage
    return pipe

# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

def generate_image(pipe: StableDiffusionPipeline, prompt: str) -> Image.Image:
    result = pipe(
        prompt=prompt,
        negative_prompt="blurry, low quality, distorted, deformed, ugly",
        num_inference_steps=30,
        guidance_scale=7.5,
        width=512,
        height=512,
    )
    return result.images[0]

# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title="AI Image Generator", layout="centered")

st.title("AI Image Generator")
st.divider()

# Prompt input — fully dynamic, no hardcoded default
prompt = st.text_area(
    label="Enter your prompt",
    placeholder="e.g. A cute Bengali girl reading a book in a cozy room, warm lighting, cinematic",
    height=100,
)

if st.button("Generate Image", type="primary", use_container_width=True):
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        try:
            # Load model (cached after first load)
            pipe = load_pipeline()

            with st.spinner("Generating image..."):
                image = generate_image(pipe, prompt.strip())

            # Save to disk
            image.save(OUTPUT_FILE)

            # Display in UI
            st.image(image, caption=f'"{prompt}"', use_container_width=True)
            st.success(f"Image saved as `{OUTPUT_FILE}`")

        except Exception as e:
            st.error(f"Error: {e}")
