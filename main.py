import os
import json
import requests
from flask import Flask, request

# --- ВАШИ НАСТРОЙКИ (Переменные заполнены) ---
# Секретный ключ удален, так как он не может быть отправлен из TradingView.
TELEGRAM_BOT_TOKEN = "5272385865:AAHk8dBbrWg2nER7TAMF76fIBaoLfEWNqpU" 
TELEGRAM_CHAT_ID = "-1002897807657" 
# ---------------------------------------------

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
    """Обрабатывает входящие Webhook-запросы от TradingView.
    Проверка ключа отключена для обхода ограничения интерфейса TV.
    """
    
    try:
        data = request.get_json(force=True)
    except Exception as e:
        # Если не удалось получить JSON, возвращаем ошибку
        return {"status": "error", "message": "Invalid JSON"}, 400

    # 1. Извлечение данных из JSON (ожидаем {{strategy.alert_message}})
    action = data.get("action")
    symbol = data.get("symbol")
    price = data.get("price")
    timeframe = data.get("timeframe")
    strategy = data.get("strategy")
    
    # 2. Форматирование сообщения для Telegram
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
    
    # Если данные неполные
    return {"status": "error", "message": "Missing data in payload"}, 400

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=PORT)
