from flask import Flask, request
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")  
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])  # Webhook should accept POST requests
def webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    reply_text = f"Ajura AI received: {text}"
    requests.post(URL, json={"chat_id": chat_id, "text": reply_text})
    
    return "OK", 200  # Ensure it returns HTTP 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
