import os
import logging
import requests
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load Telegram Bot Token securely from environment variables
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN is missing! Set it in environment variables.")

WEBHOOK_URL = "https://brain-0sv5.onrender.com/webhook"

# Function to send a message to Telegram
def send_telegram_message(chat_id, text):
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(TELEGRAM_API_URL, json=payload)

    # Log response for debugging
    logging.info(f"🔹 Forwarding to Telegram: {text}")
    if response.status_code != 200:
        logging.error(f"❌ Failed to send message: {response.text}")

    return response.json()

# Webhook route for Telegram updates
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    logging.info(f"🔹 Telegram Update Received: {update}")

    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Forwarding to Zhat GPT (Simulated)
        response = {"message": f"Ajura AI received: {text}"}
        send_telegram_message(chat_id, response["message"])

    return jsonify({"status": "ok"}), 200

# Route to receive responses from Zhat GPT
@app.route('/zhat_response', methods=['POST'])
def receive_zhat_response():
    response = request.get_json()
    logging.info(f"🔹 Zhat GPT Response Received: {response}")

    # Extract chat_id (this should be stored in a session or passed from Zhat GPT)
    chat_id = response.get("chat_id")  # Ensure chat_id is included in response
    message = response.get("message", "No message received")

    if chat_id:
        send_telegram_message(chat_id, f"Received from Zhat GPT: {message}")
    else:
        logging.error("❌ Missing chat_id in Zhat GPT response!")

    return jsonify({"status": "received"}), 200

# Test route for debugging
@app.route('/test', methods=['POST'])
def test_endpoint():
    data = request.get_json()
    logging.info(f"🔹 Received Test Message: {data}")
    return jsonify({"status": "received", "message": data}), 200

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
