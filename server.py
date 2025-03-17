import os
import openai
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot
from telegram.ext import CommandHandler, MessageHandler, filters, Updater

# Load environment variables
load_dotenv()

# Initialize Flask app and Telegram bot
app = Flask(__name__)
updater = Updater(token=os.getenv('TELEGRAM_TOKEN'))
dispatcher = updater.dispatcher
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Route for handling messages from Telegram
def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id

    # Get OpenAI response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=150
    )

    # Send the OpenAI response back to Telegram
    bot.send_message(chat_id=chat_id, text=response.choices[0].text.strip())

# Command to start bot
def start(update, context):
    update.message.reply_text("Hello, I'm your assistant!")

# Add handlers
start_handler = CommandHandler('start', start)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()

# Start the Flask app and bind to Render's PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the port provided by Render
    app.run(host="0.0.0.0", port=port, debug=True)
