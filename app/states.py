from aiogram.fsm.state import StatesGroup, State


class BudgetState(StatesGroup):
    waiting_for_budget = State()
    waiting_for_expense = State()