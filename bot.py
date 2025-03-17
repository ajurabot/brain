import telebot
from flask import Flask, request
import os

TOKEN = os.getenv("BOT_TOKEN")  # Fetching from Render environment variables
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("✅ Received Webhook")  # Debugging
    update = request.get_json()
    print(update)  # Print full update for debugging

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        print(f"📩 Message from {chat_id}: {text}")  # Debugging

        bot.send_message(chat_id, "Ajura AI is online! 🚀")  # Test reply

    return "OK", 200

if __name__ == "__main__":
    print("🚀 Bot is starting...")
    app.run(host="0.0.0.0", port=10000)
