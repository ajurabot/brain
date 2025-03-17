import logging
import openai
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up the Telegram Bot API token
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define command handlers
def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    update.message.reply_text('Hi! I am your assistant bot. Send me a message and I will process it.')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message when the /help command is issued."""
    update.message.reply_text('Send me any text and I will process it using OpenAI.')

def process_message(update: Update, context: CallbackContext) -> None:
    """Process incoming messages and get a response from OpenAI."""
    user_message = update.message.text
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_message,
            max_tokens=150
        )
        bot_reply = response.choices[0].text.strip()
        update.message.reply_text(bot_reply)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        update.message.reply_text('Sorry, I encountered an error while processing your request.')

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token
    updater = Updater(TELEGRAM_API_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
