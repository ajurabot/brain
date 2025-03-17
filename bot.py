import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your API keys from the .env file
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

# Start command to test if bot is working
async def start(update: Update, context):
    await update.message.reply_text("Hello! I am your friendly AI bot.")

# Function to handle messages and interact with OpenAI API
async def handle_message(update: Update, context):
    user_message = update.message.text
    response = openai.Completion.create(
        model="text-davinci-003",  # Example model, use the one you prefer
        prompt=user_message,
        max_tokens=150
    )
    await update.message.reply_text(response['choices'][0]['text'].strip())

# Main function to run the bot
async def main():
    # Initialize the application with your Telegram bot token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler('start', start))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    try:
        # Run the bot asynchronously
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        # Graceful shutdown (await shutdown)
        if application:
            asyncio.run(application.shutdown())
