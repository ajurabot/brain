import requests
import os
from flask import Flask, request, jsonify

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Fetching bot token from environment variable
WEBHOOK_URL = "https://brain-0sv5.onrender.com/webhook"  # Your webhook URL

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        
        if text.startswith("/test"):
            response = send_test_request()
            send_message(chat_id, response)
    
    return jsonify({"ok": True})

def send_test_request():
    """Send a test request to your webhook and return the response."""
    try:
        res = requests.post(WEBHOOK_URL, json={"message": {"chat": {"id": 123456}, "text": "Hello!"}})
        return res.text
    except Exception as e:
        return f"Error: {e}"

def send_message(chat_id, text):
    """Send a message back to the user."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
