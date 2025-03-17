import os
import telebot
import openai
from flask import Flask, request

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CHAT_ID = os.getenv("CHAT_ID")
PORT = int(os.getenv("PORT", 10000))  # Default to 10000 if not set

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize Flask App
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handles incoming Telegram messages."""
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

@bot.message_handler(commands=['start'])
def start_command(message):
    """Responds to /start command."""
    bot.send_message(message.chat.id, "Ajura AI Activated! How can I assist you?")

@bot.message_handler(func=lambda msg: True)
def chat_with_ai(message):
    """Handles all text messages and replies using OpenAI."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message.text}]
    )
    bot.send_message(message.chat.id, response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    # Set Webhook for Telegram Bot
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

    # Start Flask App
    app.run(host="0.0.0.0", port=PORT)
