import os
import json
import requests
import openai
from flask import Flask, request

app = Flask(__name__)

# Get environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API client
openai.api_key = OPENAI_API_KEY

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

    # Query OpenAI API for a response to the user's message
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can replace with any GPT model you prefer
        prompt=message_text,
        max_tokens=150
    )

    # Extract the AI response
    ai_response = response.choices[0].text.strip()

    # Send the AI response back to the user on Telegram
    send_message_url = f"{TELEGRAM_API_URL}/sendMessage"
    response_message = f"Ajura AI received: {ai_response}"
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
    app.run(host='0.0.0.0', port=10000, debug=True)
