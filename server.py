import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Load token securely from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    
    # Send response
    response_text = f"Ajura AI received: {text}"
    requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": response_text})

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
