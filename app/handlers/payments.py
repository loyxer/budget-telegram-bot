from aiogram import F, Router
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from app.config import PREMIUM_DURATION_DAYS, PREMIUM_STARS_PRICE
from app.db import grant_premium

router = Router()


@router.callback_query(F.data == "buy_premium")
async def buy_premium(callback: CallbackQuery):
    await callback.message.answer_invoice(
        title="Підписка на конспекти",
        description=f"Необмежені конспекти на {PREMIUM_DURATION_DAYS} днів.",
        payload="premium_subscription",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Підписка", amount=PREMIUM_STARS_PRICE)],
    )
    await callback.answer()


@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    grant_premium(message.from_user.id, PREMIUM_DURATION_DAYS)
    await message.answer(f"Дякую! Підписку активовано на {PREMIUM_DURATION_DAYS} днів ⭐")
