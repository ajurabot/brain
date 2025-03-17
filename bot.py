import logging
import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()  # Load environment variables from .env

# Load your Telegram bot token and OpenAI key from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the /start command handler
async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm your assistant bot powered by Ajura AI!")

# Define a function to handle text messages and pass them to OpenAI's API
async def handle_message(update: Update, context):
    user_message = update.message.text

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Change engine if you want to use a different model
            prompt=user_message,
            max_tokens=150
        )
        await update.message.reply_text(response['choices'][0]['text'].strip())
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await update.message.reply_text("Sorry, something went wrong!")

# Define the main function that sets up the bot and starts the event loop
async def main():
    # Create the application instance
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))

    # Add message handler for handling user messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    try:
        await application.run_polling()
    except Exception as e:
        logger.error(f"Error during bot execution: {e}")
    finally:
        await application.shutdown()

# Ensure to handle async execution properly when running
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
