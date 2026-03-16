from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime

from app.states import BudgetState
from app.db import set_budget
from app.keyboards.main import main_keyboard

router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "Hello! I am your budget bot 💰\nChoose an action below.",
        reply_markup=main_keyboard
    )


@router.message(F.text == "Start Budget")
async def start_budget(message: Message, state: FSMContext):
    await message.answer("How much money do you want to start with for the next 30 days?")
    await state.set_state(BudgetState.waiting_for_budget)


@router.message(BudgetState.waiting_for_budget)
async def process_budget(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Please send only a number. Example: 2000")
        return

    set_budget(message.chat.id, amount, datetime.now().isoformat())
    await state.clear()

    await message.answer(
        f"Budget started: {amount}€ for 30 days.",
        reply_markup=main_keyboard
    )