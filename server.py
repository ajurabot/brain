from flask import Flask, request
import os
import requests

# Initialize Flask app
app = Flask(__name__)

# Get Telegram Bot Token from environment variable
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route("/", methods=["GET"])
def home():
    return "Ajura AI is Live!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    """Handles incoming Telegram messages."""
    data = request.json
    print("Received:", data)  # Log the incoming message

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Reply back to Telegram
        reply_message = {
            "chat_id": chat_id,
            "text": f"Received: {text}"
        }
        requests.post(TELEGRAM_API_URL, json=reply_message)

    return {"status": "ok"}, 200  # Respond to Telegram

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
