import os
import openai
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Load environment variables
load_dotenv()

# Initialize Flask app and Telegram bot
app = Flask(__name__)

# Initialize Telegram Application
application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Route for handling messages from Telegram
async def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id

    # Get OpenAI response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=150
    )

    # Send the OpenAI response back to Telegram
    await context.bot.send_message(chat_id=chat_id, text=response.choices[0].text.strip())

# Command to start bot
async def start(update, context):
    await update.message.reply_text("Hello, I'm your assistant!")

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Start the bot
application.run_polling()

# Start the Flask app and bind to Render's PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the port provided by Render
    app.run(host="0.0.0.0", port=port, debug=True)
