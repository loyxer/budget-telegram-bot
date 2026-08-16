import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import BOT_TOKEN
from app.db import init_db
from app.handlers.payments import router as payments_router
from app.handlers.start import router as start_router
from app.handlers.summarize import router as summarize_router


async def main():
    logging.basicConfig(level=logging.INFO)

    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задано. Скопіюй .env.example у .env і заповни його.")

    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(payments_router)
    dp.include_router(summarize_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
