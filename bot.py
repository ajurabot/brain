import os
import openai
import telebot
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CHAT_ID = os.getenv("CHAT_ID")

# Initialize OpenAI and Telegram bot
openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Flask server to handle Telegram webhook
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        if str(chat_id) == CHAT_ID:  # Ensure only you can use the bot
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": text}]
            )
            reply = response["choices"][0]["message"]["content"]
            bot.send_message(chat_id, reply)
        else:
            bot.send_message(chat_id, "Unauthorized access!")
    
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
