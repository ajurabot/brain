from flask import Flask, request
import requests

app = Flask(__name__)

# Telegram Bot Token
TOKEN = "8132210933:AAFSnHuBpO6LcZ-S4DPGcvyXxOas_yKjb24"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram messages."""
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # Process the received message and generate a response
        response_text = process_message(text)

        # Send the response back to the user
        send_message(chat_id, response_text)

    return "OK", 200

def process_message(text):
    """Process the incoming message and determine the response."""
    # Modify this function to make Ajura AI smarter
    return f"Ajura AI received: {text}"

def send_message(chat_id, text):
    """Send a message to the specified chat."""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
