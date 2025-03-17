import telebot
import openai
import json
import os
from flask import Flask, request

# Load tokens from environment
TOKEN = os.getenv("BOT_TOKEN")  # Ensure this is set in Render
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

MEMORY_FILE = "memory.json"

# Load and save memory functions
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file)

memory = load_memory()

# Flask setup
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

# Handle start/help command
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Ajura AI! Send me a message and I'll respond.")

# Handle normal messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = str(message.chat.id)
    user_input = message.text

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({"role": "user", "content": user_input})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=memory[user_id]
        )
        reply = response["choices"][0]["message"]["content"]
        memory[user_id].append({"role": "assistant", "content": reply})
        save_memory(memory)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Sorry, something went wrong: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
