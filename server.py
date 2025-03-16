from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ✅ Get token and chat ID from environment variables
TOKEN = os.getenv("TOKEN")  # Your Telegram bot token
CHAT_ID = os.getenv("CHAT_ID")  # Your personal Telegram chat ID

# ✅ Function to send messages anytime
def send_message(text):
    if TOKEN and CHAT_ID:  # Ensure the environment variables are set
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

        # ✅ Echo the received message
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
