# conspect-bot

Telegram-бот, який робить стислі конспекти з тексту, посилань на статті або PDF/TXT файлів.

- **Безкоштовно**: обмежена кількість конспектів на день, обмежений розмір тексту.
- **Підписка**: без денного ліміту, довші тексти. Оплата — Telegram Stars, прямо в чаті.
- **AI-частина** — не хмарний API, а безкоштовна відкрита модель ([Ollama](https://ollama.com)), яка працює прямо на твоєму сервері. Жодних платежів за запити.

## Локальний запуск

1. Встанови [Ollama](https://ollama.com/download) і завантаж модель:
   ```bash
   ollama pull qwen2.5:3b
   ```
   (Ollama сама піднімає локальний сервер на `localhost:11434` після встановлення.)
2. Встанови залежності бота:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Скопіюй `.env.example` у `.env` і заповни `BOT_TOKEN` (від @BotFather). Значення `OLLAMA_HOST`/`OLLAMA_MODEL` можна лишити за замовчуванням.
4. Запусти бота:
   ```bash
   python main.py
   ```

## Деплой на власний сервер (без Railway/PaaS)

Приклад для звичайного VPS з Ubuntu/Debian.

```bash
# Ollama — офіційний скрипт встановлення, одразу ставить себе як systemd-сервіс
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:3b

sudo apt update && sudo apt install -y python3-venv git
git clone <адреса_репо> conspect-bot
cd conspect-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # і заповнити BOT_TOKEN
```

> Про "залізо": `qwen2.5:3b` комфортно працює навіть на CPU-only VPS з 4+ ГБ RAM (відповідь — кілька-десятки секунд). Якщо на сервері є більше RAM і потрібна краща якість, можна поставити важчу модель (`ollama pull qwen2.5:7b`) і вказати її в `OLLAMA_MODEL`.

Створи systemd-сервіс `/etc/systemd/system/conspect-bot.service`:

```ini
[Unit]
Description=conspect-bot
After=network.target ollama.service
Requires=ollama.service

[Service]
Type=simple
User=<твій_користувач>
WorkingDirectory=/home/<твій_користувач>/conspect-bot
EnvironmentFile=/home/<твій_користувач>/conspect-bot/.env
ExecStart=/home/<твій_користувач>/conspect-bot/venv/bin/python main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Потім:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now conspect-bot
sudo journalctl -u conspect-bot -f   # логи
```

Бот працює через `polling` — вихідний зв'язок з Telegram API, окремий домен/порт не потрібен.

## Структура проєкту

```
main.py                    # точка входу
app/config.py               # змінні оточення, ліміти, ціна підписки
app/db.py                    # SQLite: денний ліміт і статус підписки
app/keyboards.py             # inline-кнопка оформлення підписки
app/services/extractor.py    # витяг тексту з URL / PDF
app/services/summarizer.py   # виклик локальної моделі через Ollama
app/handlers/start.py        # /start, /status
app/handlers/summarize.py    # обробка тексту / файлів / посилань
app/handlers/payments.py     # оплата через Telegram Stars
```
