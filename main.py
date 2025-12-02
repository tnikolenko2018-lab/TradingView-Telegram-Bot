import os
import json
import requests
from flask import Flask, request
# Убедитесь, что эти 4 переменные есть
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
app = Flask(__name__)
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

**2. Проверьте извлечение данных (внутри функции `tradingview_webhook`):**
Ваш сервер должен принимать **все 6 полей** от нового автоматического бота.

```python
    action = data.get("action")
    symbol = data.get("symbol")
    entry_high = data.get("entry_high")
    entry_low = data.get("entry_low")
    stop_loss = data.get("stop_loss")  # Обязательно должно быть
    tp1 = data.get("tp1")              # Обязательно должно быть

**3. Проверьте форматирование сообщения Telegram:**

```python
        message_text = (
            f"⚡️ *СИГНАЛ: AUTO S/R FLIP {emoji}*\n"
            f"**Инструмент:** {symbol}\n"
            f"**Действие:** **{color_text}**\n\n"
            f"**🎯 Зона Входа:** `{entry_low}` – `{entry_high}`\n"
            f"**🛑 Стоп-Лосс:** `{stop_loss}`\n"
            f"**✅ Тейк-Профит:** `{tp1}`\n"
        )
