import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-5")

DB_PATH = os.getenv("DB_PATH", "bot.db")

FREE_DAILY_LIMIT = 5
FREE_MAX_CHARS = 8000
PREMIUM_MAX_CHARS = 60000

PREMIUM_STARS_PRICE = 150
PREMIUM_DURATION_DAYS = 30
