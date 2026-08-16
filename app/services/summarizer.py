from anthropic import AsyncAnthropic

from app.config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL

client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = (
    "Ти асистент, який робить стислі конспекти текстів українською мовою. "
    "Виділяй головні тези у вигляді маркованого списку, без вступних фраз і повторів."
)


async def summarize(text: str) -> str:
    response = await client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        thinking={"type": "disabled"},
        output_config={"effort": "low"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Зроби конспект цього тексту:\n\n{text}"}],
    )

    if response.stop_reason == "refusal":
        raise ValueError("Модель відмовилась опрацьовувати цей текст.")

    return next(block.text for block in response.content if block.type == "text")
