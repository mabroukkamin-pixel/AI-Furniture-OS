from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv(
    override=True
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


OUTPUT_DIR = PROJECT_ROOT / "outputs"


DEFAULT_ENGINE = "nano_banana"


IMAGE_SIZE = "1024x1024"

IMAGE_QUALITY = "high"


TIMEOUT = 300

MAX_RETRIES = 3


LOG_LEVEL = "INFO"


# AI Providers

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL"
)


def is_gemini_configured():

    api_key = (
        GEMINI_API_KEY or ""
    ).strip()

    model = (
        GEMINI_MODEL or ""
    ).strip()

    return (
        api_key.startswith("AIza")
        and len(api_key) > 30
        and bool(model)
    )


# Nano Banana
NANO_BANANA_API_KEY = os.getenv(
    "NANO_BANANA_API_KEY"
)
NANO_BANANA_BASE_URL = os.getenv(
    "NANO_BANANA_BASE_URL"
)
NANO_BANANA_MODEL = os.getenv(
    "NANO_BANANA_MODEL"
)