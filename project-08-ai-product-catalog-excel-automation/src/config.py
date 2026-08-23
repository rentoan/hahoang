from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]
MAPPING_CONFIG = BASE_DIR / "mapping_config.json"

ALLOWED_CATEGORIES = {
    "Electrical",
    "Hand Tools",
    "Lighting",
    "Power Tools",
    "Safety",
    "Storage",
}

MAX_TITLE_LENGTH = 80

AI_MODE = os.getenv("AI_MODE", "mock").lower()   # mock | openai
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")
