from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv(dotenv_path=Path(".") / ".env")

MODEL_NAME = "gpt-4.1-mini"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MAX_MIN_PER_DAY = 50
DEFAULT_PLAN_DAYS = 40
MIN_PLAN_DAYS = 3
MAX_PLAN_DAYS = 120
MAX_ITERATIONS = 5

MEMORY_FILE = "data/study_memory.json"