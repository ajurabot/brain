from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Root route to verify the server is running
@app.route('/')
def home():
    return "Ajura AI is running!", 200

# Webhook route to handle Telegram messages
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        reply_text = f"Ajura AI received: {text}"
        send_message(chat_id, reply_text)
    return "OK", 200

def send_message(chat_id, text):
    token = os.getenv('BOT_TOKEN')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
