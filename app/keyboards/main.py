from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start Budget")],
        [KeyboardButton(text="Add Expense")],
        [KeyboardButton(text="Show Stats")]
    ],
    resize_keyboard=True
)