import telebot
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("ERROR: Telegram bot TOKEN is missing!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Your bot is running successfully.")

if __name__ == "__main__":
    bot.polling()
