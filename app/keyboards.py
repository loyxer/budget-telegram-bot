from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.config import PREMIUM_STARS_PRICE

upgrade_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"⭐ Оформити підписку за {PREMIUM_STARS_PRICE} Stars",
                callback_data="buy_premium",
            )
        ]
    ]
)
