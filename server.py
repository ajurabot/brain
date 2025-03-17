import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Command to start bot
async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm your assistant bot. Type anything to interact with me.")

# Handling text messages
async def handle_message(update: Update, context):
    user_message = update.message.text
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_message,
        max_tokens=150
    )
    await update.message.reply_text(response.choices[0].text.strip())

# Main function to set up the bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start webhook with updated URL
    port = int(os.environ.get('PORT', 5000))
    application.run_webhook(listen="0.0.0.0", port=port, url_path=TELEGRAM_TOKEN, webhook_url=f"https://brain-0sv5.onrender.com/{TELEGRAM_TOKEN}")

if __name__ == "__main__":
    main()
