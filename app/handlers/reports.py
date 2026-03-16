from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime

from app.db import get_budget

router = Router()


@router.message(F.text == "Show Stats")
async def show_stats(message: Message):
    data = get_budget(message.chat.id)

    if not data:
        await message.answer("No active budget. Start one first.")
        return

    start_budget, spent, start_date = data
    remaining = start_budget - spent
    percent = (remaining / start_budget) * 100

    start_dt = datetime.fromisoformat(start_date)
    days_passed = (datetime.now() - start_dt).days
    days_left = 30 - days_passed

    if days_left < 0:
        days_left = 0

    await message.answer(
        f"📊 Budget Stats\n\n"
        f"Start budget: {start_budget}€\n"
        f"Spent: {spent}€\n"
        f"Remaining: {remaining}€\n"
        f"Saved percent: {percent:.2f}%\n"
        f"Days left: {days_left}"
    )