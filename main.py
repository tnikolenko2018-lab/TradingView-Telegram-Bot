import os
import json
import requests
from flask import Flask, request

# --- ВАШИ НАСТРОЙКИ (Переменные заполнены) ---
TELEGRAM_BOT_TOKEN = "5272385865:AAHk8dBbrWg2nER7TAMF76fIBaoLfEWNqpU" 
TELEGRAM_CHAT_ID = "-1002897807657" 
# 1. Проверка Секретного Ключа (Security Check)
    received_secret = request.headers.get('Authorization')
    if received_secret != f"Bearer {WEBHOOK_SECRET}":
        return {"status": "error", "message": "Invalid secret"}, 403

app = Flask(__name__)
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_telegram_message(text):
    """Отправляет отформатированное сообщение в Telegram."""
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }
    try:
        requests.post(TELEGRAM_API_URL, data=payload)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке в Telegram: {e}")

@app.route('/webhook/tradingview', methods=['POST'])
def tradingview_webhook():
# 1. Проверка Секретного Ключа (Security Check)
    received_secret = request.headers.get('Authorization')
    if received_secret != f"Bearer {WEBHOOK_SECRET}":
        return {"status": "error", "message": "Invalid secret"}, 403
# TELEGRAM_CHAT_ID = "-1002897807657"  <-- Ваше значение
# WEBHOOK_SECRET = "SmartMoney2025Secret"  <-- ЭТУ СТРОКУ НУЖНО УДАЛИТЬ ИЛИ ЗАКОММЕНТИРОВАТЬ
# ---------------------
        return {"status": "error", "message": "Invalid secret"}, 403

    try:
        data = request.get_json(force=True)
    except Exception as e:
        return {"status": "error", "message": "Invalid JSON"}, 400

    # 2. Извлечение данных из JSON
    action = data.get("action")
    symbol = data.get("symbol")
    price = data.get("price")
    timeframe = data.get("timeframe")
    strategy = data.get("strategy")
    
    # 3. Форматирование сообщения для Telegram
    if action and symbol and price:
        emoji = "🟢 BUY" if action == "BUY" else "🔴 SELL"
        color = "BUY" if action == "BUY" else "SELL"
        
        message_text = (
            f"🔔 *НОВЫЙ СИГНАЛ: {emoji} {symbol}*\n\n"
            f"**Стратегия:** {strategy} ({timeframe})\n"
            f"**Действие:** **{color}**\n"
            f"**Цена входа:** `{price}`\n\n"
        )
        send_telegram_message(message_text)
        return {"status": "success", "message": "Signal processed and sent"}, 200
    
    return {"status": "error", "message": "Missing data in payload"}, 400

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=PORT)
