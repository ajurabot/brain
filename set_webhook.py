import telebot
import os

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)

if not WEBHOOK_URL:
    raise ValueError("ERROR: Webhook URL is missing!")

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

print("Webhook set successfully!")
