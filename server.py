import os
import logging
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load Telegram token and chat ID from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram updates."""
    try:
        update = request.get_json()
        logging.info(f"Received update: {update}")

        # Extract message if available
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")

            # Send acknowledgment back to Telegram
            send_message(chat_id, f"Received: {text}")

        return jsonify({"ok": True}), 200

    except Exception as e:
        logging.error(f"Error handling update: {str(e)}")
        return jsonify({"ok": False, "error": str(e)}), 500

def send_message(chat_id, text):
    """Send a message back to Telegram."""
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    logging.info(f"Sent message response: {response.json()}")
    return response.json()

# Root route (for health check)
@app.route('/', methods=['GET'])
def index():
    return "Ajura AI Webhook is Live!", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
