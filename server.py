import os
import logging
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Telegram Bot Token (Make sure it's set in Render's environment variables)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

@app.route('/')
def home():
    return "Ajura AI is live!", 200

# ✅ FIXED: Webhook now accepts **POST requests**
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    logging.info(f"Received update: {update}")

    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Replying back to Telegram
        reply_text = f"Ajura AI received: {text}"
        send_telegram_message(chat_id, reply_text)

    return jsonify({"status": "ok"}), 200

# Function to send messages to Telegram
def send_telegram_message(chat_id, text):
    import requests
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(TELEGRAM_API_URL, json=payload)
    
    if response.status_code != 200:
        logging.error(f"Failed to send message: {response.text}")

    return response.json()

# Start the Flask server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
