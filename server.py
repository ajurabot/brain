import os
import logging
from flask import Flask, request, jsonify
import requests

# Initialize Flask app
app = Flask(__name__)

# Telegram Bot Token (Set this as an environment variable)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No Telegram Bot Token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        # Process user message and send a response
        reply_text = f"Ajura AI received: {text}"
        send_telegram_message(chat_id, reply_text)
    return jsonify({"status": "ok"}), 200

# Function to send messages to Telegram
def send_telegram_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(TELEGRAM_API_URL, json=payload)
    if response.status_code != 200:
        logging.error(f"Failed to send message: {response.text}")
    return response.json()

# Root route for testing
@app.route('/')
def home():
    return "Ajura AI is live!", 200

# Run the Flask app
if __name__ == '__main__':
    # Set logging level
    logging.basicConfig(level=logging.INFO)
    # Ensure the port is read from the environment for Render compatibility
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
