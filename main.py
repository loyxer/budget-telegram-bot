import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlers.start import router as start_router
from app.handlers.add import router as add_router
from app.handlers.reports import router as reports_router


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token="8372379962:AAFT2phShOoDTL3UDZVYo46LyCg6bHKbVfw")
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(add_router)
    dp.include_router(reports_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())