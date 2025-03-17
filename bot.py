import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from .env file
load_dotenv()

# Telegram bot token from the environment
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to start the bot and send a greeting message
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_html(f'Hello, {user.mention_html()}! Welcome to the Ajura Bot!')

# Function to handle messages and pass them to OpenAI API for responses
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    try:
        # Request response from OpenAI model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        # Get the model's response and send it back to the user
        bot_reply = response['choices'][0]['message']['content']
        await update.message.reply_text(bot_reply)
    
    except Exception as e:
        logger.error(f"Error with OpenAI API: {e}")
        await update.message.reply_text("Sorry, something went wrong with processing your request.")

# Main function to run the bot
async def main():
    # Create the application and pass in the token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl+C or the process is stopped
    await application.run_polling()

# To handle graceful shutdown
async def shutdown_application(application: Application):
    await application.shutdown()

# Run the bot with the event loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot shutting down...")
        shutdown_application(application)
