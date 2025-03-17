import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve API keys from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Define command handler functions
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your AI assistant. How can I help you today?')

def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Send me a message, and I will respond using OpenAI.')

def handle_message(update: Update, _: CallbackContext) -> None:
    user_message = update.message.text
    try:
        # Call OpenAI API to get a response
        response = openai.Completion.create(
            model="text-davinci-003",  # Use a suitable model
            prompt=user_message,
            max_tokens=150
        )
        ai_message = response.choices[0].text.strip()
        update.message.reply_text(ai_message)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        update.message.reply_text('Sorry, I encountered an error while processing your request.')

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token
    updater = Updater(TELEGRAM_API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
