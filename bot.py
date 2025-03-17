import os
import telebot
from flask import Flask, request

# Load Telegram Bot Token from Render environment variable
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Initialize Flask app
app = Flask(__name__)

# Webhook route to receive updates from Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = request.get_json()
        if update:
            bot.process_new_updates([telebot.types.Update.de_json(update)])
        return 'OK', 200  # Always return 200 for Telegram
    except Exception as e:
        print(f"Error: {str(e)}")
        return 'Internal Server Error', 500

# Test route to check if the server is running
@app.route('/')
def home():
    return 'Bot is running!', 200

# Start Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
