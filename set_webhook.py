import os
import telebot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
bot.remove_webhook()
bot.set_webhook(url=f"{WEBHOOK_URL}")

print("✅ Webhook Set Successfully!")
