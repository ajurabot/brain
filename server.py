from flask import Flask, request
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")  # Fetch token from environment
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    # Auto-reply logic
    reply_text = f"Ajura AI received: {text}"
    
    requests.post(URL, json={"chat_id": chat_id, "text": reply_text})
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
