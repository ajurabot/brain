import os
import openai
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

openai.api_key = OPENAI_API_KEY

@app.route('/api/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')

    # Generate response from OpenAI
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=150
    )

    reply = response.choices[0].text.strip()

    # Send response to Telegram
    telegram_data = {
        'chat_id': user_id,
        'text': reply
    }
    requests.post(TELEGRAM_API_URL, data=telegram_data)

    return jsonify({'status': 'Message sent to Telegram'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
