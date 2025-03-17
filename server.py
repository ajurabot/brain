import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Your Telegram bot token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Telegram API URL
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()  # Parse incoming request

    # Get the chat_id and the message text
    chat_id = update['message']['chat']['id']
    message_text = update['message']['text']
    
    # Print the received message (for debugging)
    print(f"Received message: {message_text} from chat_id: {chat_id}")
    
    # Send a reply to the user
    response_message = f"Ajura AI received: {message_text}"
    
    # Make a request to send the response back to the user
    send_message_url = f"{TELEGRAM_API_URL}/sendMessage"
    response = requests.post(send_message_url, data={
        'chat_id': chat_id,
        'text': response_message
    })

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
