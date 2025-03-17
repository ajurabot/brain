from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Ensure this is set in Render
CHAT_ID = os.getenv("CHAT_ID")  # Optional, for testing responses

# Webhook route (Handles Telegram Updates)
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("✅ Received Telegram update:", data)  # Debugging purposes

    # Ensure data contains a message
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # Simple auto-response
        send_message(chat_id, f"🤖 Ajura AI received: {text}")

    return "OK", 200  # Must return 200 OK to Telegram

# Function to send messages via Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    print("📩 Message sent response:", response.json())  # Debugging
    return response.json()

# Root route for testing if the server is alive
@app.route("/", methods=["GET"])
def home():
    return "Ajura AI is live ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
