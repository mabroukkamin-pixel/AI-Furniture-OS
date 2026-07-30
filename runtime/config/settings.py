from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


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