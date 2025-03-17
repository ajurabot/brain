import logging
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Telegram Bot Token from BotFather
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Set up logging to get visibility of what's happening
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your assistant bot, ready to chat.')

# Function to handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Get the user's message
    response = get_openai_response(user_message)
    update.message.reply_text(response)

# Function to generate a response using OpenAI API
def get_openai_response(user_message: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the appropriate model here
            prompt=user_message,
            max_tokens=150
        )
        return response.choices[0].text.strip()  # Return the text of the first choice
    except Exception as e:
        logger.error(f"Error processing OpenAI request: {e}")
        return "Sorry, I couldn't process your request."

# Function to set up the updater and dispatcher
def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Add command handler for /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Add message handler for regular messages
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
