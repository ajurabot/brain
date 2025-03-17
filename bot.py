import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up API keys
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle /start command
async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm your assistant, Ajura AI! 🤖💡")

# Function to handle messages
async def handle_message(update: Update, context):
    user_message = update.message.text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=100
    )
    ai_response = response.choices[0].text.strip()
    await update.message.reply_text(ai_response)

# Main function to set up the bot
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
