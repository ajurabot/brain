import telebot
import openai
import json
import os
from flask import Flask, request

# Load environment variables
TOKEN = os.getenv("BOT_TOKEN")  # Ensure correct in Render
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

MEMORY_FILE = "memory.json"

# Load and save memory functions
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file)

memory = load_memory()

# Flask setup for Webhook
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Ajura AI Bot is Live!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

# Start and Help Commands
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Ajura AI! I'm here to assist you. Type anything and I'll respond.")

# Message Handling
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = str(message.chat.id)
    user_input = message.text.strip()

    if not user_input:
        bot.reply_to(message, "Your message is empty. Please send a valid text.")
        return

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Change to "gpt-3.5-turbo" if limited by API access
            messages=memory[user_id]
        )
        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"Error processing your request: {str(e)}"

    memory[user_id].append({"role": "assistant", "content": reply})
    save_memory(memory)

    bot.reply_to(message, reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Ensure the port matches Render settings
