from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ✅ Replace with your actual bot token and chat ID
TOKEN = "your_telegram_bot_token"
CHAT_ID = "your_chat_id"

# ✅ Function to send messages anytime
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

# ✅ Webhook route to handle incoming messages
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        user_text = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        # ✅ Echo the received message for now (you can upgrade this later)
        response_text = f"Ajura AI received: {user_text}"
        send_message(response_text)  # Send response

    return {"ok": True}

# ✅ Root route to check if the bot is running
@app.route('/')
def home():
    return "🔥 Ajura AI is working!"

# ✅ Run Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
