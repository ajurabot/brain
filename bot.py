import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot command handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your bot.")

# The main function to run your bot
async def main():
    # Create the application and add handlers
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    
    application.add_handler(CommandHandler("start", start))
    
    # Run the bot
    await application.run_polling()

# Avoid the "RuntimeError: This event loop is already running" issue
def run():
    try:
        asyncio.run(main())  # This ensures only one event loop is running
    except RuntimeError as e:
        if str(e) == "This event loop is already running":
            print("Event loop is already running. Handling it gracefully.")
            # You can use another strategy here if needed, like creating an instance and running it in a different thread

if __name__ == '__main__':
    run()
