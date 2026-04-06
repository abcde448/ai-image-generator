"""
config.py - Central configuration for the AI Image Generator.
Tweak these values without touching core logic.
"""

# Default prompt used when none is provided via CLI or input()
DEFAULT_PROMPT = (
    "A cute young Bengali girl wearing a saree, with round glasses, "
    "reading a book in a cozy room with warm lighting, "
    "highly detailed, cinematic, realistic."
)

# OpenAI image generation settings
MODEL        = "gpt-image-1"
IMAGE_SIZE   = "1024x1024"   # "1024x1024" | "1536x1024" | "1024x1536"
IMAGE_QUALITY = "high"       # "low" | "medium" | "high"

# Local output
OUTPUT_DIR   = "output"
IMAGE_FORMAT = "png"
