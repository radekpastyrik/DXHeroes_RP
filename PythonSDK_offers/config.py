from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
BASE_URL = os.environ["BASE_URL"]
REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
TOKEN_CACHE_PATH = Path(".auth_token_cache.json")
TOKEN_VALIDITY_SECONDS = 5 * 60  # token valid 5 min