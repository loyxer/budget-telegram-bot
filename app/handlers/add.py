from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.states import BudgetState
from app.db import add_expense, get_budget
from app.keyboards.main import main_keyboard

router = Router()


@router.message(F.text == "Add Expense")
async def add_expense_start(message: Message, state: FSMContext):
    data = get_budget(message.chat.id)

    if not data:
        await message.answer("First start a budget using the 'Start Budget' button.")
        return

    await message.answer("Send the expense amount.")
    await state.set_state(BudgetState.waiting_for_expense)


@router.message(BudgetState.waiting_for_expense)
async def process_expense(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Please send only a number. Example: 50")
        return

    add_expense(message.chat.id, amount)
    budget = get_budget(message.chat.id)

    start_budget, spent, start_date = budget
    remaining = start_budget - spent

    await state.clear()

    await message.answer(
        f"Expense added: {amount}€\n"
        f"Total spent: {spent}€\n"
        f"Remaining: {remaining}€",
        reply_markup=main_keyboard
    )