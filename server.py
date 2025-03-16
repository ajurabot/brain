from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Load Telegram Bot Token from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route('/')
def home():
    return "Ajura AI is working!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        # Respond back to Telegram
        send_message(chat_id, f"Ajura AI received: {text}")

    return "OK", 200  # Make sure Telegram gets a valid response

def send_message(chat_id, text):
    """Send a message to Telegram chat"""
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(TELEGRAM_API_URL, json=data)
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
