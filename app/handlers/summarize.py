from aiogram import F, Router
from aiogram.types import Message

from app.config import FREE_DAILY_LIMIT, FREE_MAX_CHARS, PREMIUM_MAX_CHARS
from app.db import is_premium, register_usage, remaining_free
from app.keyboards import upgrade_keyboard
from app.services.extractor import extract_from_pdf, extract_from_url, is_url
from app.services.summarizer import summarize

router = Router()

MIN_TEXT_LENGTH = 200


async def _has_free_uses_left(message: Message) -> bool:
    user_id = message.from_user.id
    if is_premium(user_id):
        return True
    if remaining_free(user_id, FREE_DAILY_LIMIT) <= 0:
        await message.answer(
            "Безкоштовний ліміт на сьогодні вичерпано 😔\n"
            "Оформи підписку, щоб знімати обмеження.",
            reply_markup=upgrade_keyboard,
        )
        return False
    return True


async def _run_summary(message: Message, text: str) -> None:
    user_id = message.from_user.id
    max_chars = PREMIUM_MAX_CHARS if is_premium(user_id) else FREE_MAX_CHARS

    if len(text) > max_chars:
        text = text[:max_chars]
        await message.answer(f"⚠️ Текст обрізано до {max_chars} символів для твого тарифу.")

    status = await message.answer("Роблю конспект…")
    try:
        result = await summarize(text)
    except Exception as exc:
        await status.edit_text(f"Не вдалося зробити конспект: {exc}")
        return

    if not is_premium(user_id):
        register_usage(user_id)

    await status.edit_text(result)


@router.message(F.document)
async def handle_document(message: Message):
    if not await _has_free_uses_left(message):
        return

    doc = message.document
    file = await message.bot.get_file(doc.file_id)
    file_bytes = await message.bot.download_file(file.file_path)
    data = file_bytes.read()

    name = (doc.file_name or "").lower()
    try:
        if name.endswith(".pdf"):
            text = extract_from_pdf(data)
        elif name.endswith(".txt"):
            text = data.decode("utf-8", errors="ignore")
        else:
            await message.answer("Підтримую тільки PDF та TXT файли.")
            return
    except ValueError as exc:
        await message.answer(str(exc))
        return

    await _run_summary(message, text)


@router.message(F.text)
async def handle_text(message: Message):
    if not await _has_free_uses_left(message):
        return

    text = message.text.strip()

    if is_url(text):
        try:
            text = extract_from_url(text)
        except ValueError as exc:
            await message.answer(str(exc))
            return
    elif len(text) < MIN_TEXT_LENGTH:
        await message.answer(
            f"Надішли довший текст (від ~{MIN_TEXT_LENGTH} символів), "
            "посилання на статтю або PDF/TXT файл."
        )
        return

    await _run_summary(message, text)
