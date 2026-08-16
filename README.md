# conspect-bot

Telegram-бот, який робить стислі конспекти з тексту, посилань на статті або PDF/TXT файлів.

- **Безкоштовно**: обмежена кількість конспектів на день, обмежений розмір тексту.
- **Підписка**: без денного ліміту, довші тексти. Оплата — Telegram Stars, прямо в чаті.

## Локальний запуск

1. Встанови залежності:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Скопіюй `.env.example` у `.env` і заповни:
   ```
   BOT_TOKEN=      # токен від @BotFather
   ANTHROPIC_API_KEY=
   ANTHROPIC_MODEL=claude-opus-5   # можна замінити на claude-haiku-4-5 для дешевших запитів
   ```
3. Запусти бота:
   ```bash
   python main.py
   ```

## Деплой на власний сервер (без Railway/PaaS)

Приклад для звичайного VPS з Ubuntu/Debian.

```bash
sudo apt update && sudo apt install -y python3-venv git
git clone <адреса_репо> conspect-bot
cd conspect-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # і заповнити значення
```

Створи systemd-сервіс `/etc/systemd/system/conspect-bot.service`:

```ini
[Unit]
Description=conspect-bot
After=network.target

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
app/services/summarizer.py   # виклик Claude API
app/handlers/start.py        # /start, /status
app/handlers/summarize.py    # обробка тексту / файлів / посилань
app/handlers/payments.py     # оплата через Telegram Stars
```
