import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

DB_PATH = os.getenv("DB_PATH", "bot.db")

FREE_DAILY_LIMIT = 5
FREE_MAX_CHARS = 8000
PREMIUM_MAX_CHARS = 60000

PREMIUM_STARS_PRICE = 150
PREMIUM_DURATION_DAYS = 30
