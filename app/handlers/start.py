from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config import FREE_DAILY_LIMIT, FREE_MAX_CHARS
from app.db import is_premium, remaining_free

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привіт! Я роблю стислі конспекти 📝\n\n"
        "Надішли мені:\n"
        "• текст\n"
        "• посилання на статтю\n"
        "• PDF або TXT файл\n\n"
        f"Безкоштовно — до {FREE_DAILY_LIMIT} конспектів на день "
        f"(текст до {FREE_MAX_CHARS} символів).\n"
        "Команда /status покаже, скільки лишилось."
    )


@router.message(Command("status"))
async def cmd_status(message: Message):
    user_id = message.from_user.id
    if is_premium(user_id):
        await message.answer("У тебе активна підписка ⭐ — без денного ліміту.")
        return

    left = remaining_free(user_id, FREE_DAILY_LIMIT)
    await message.answer(f"Залишилось безкоштовних конспектів сьогодні: {left}/{FREE_DAILY_LIMIT}")
