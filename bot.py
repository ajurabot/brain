import telebot
import openai
import json
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file)

memory = load_memory()

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Ajura AI! Send me a message and I'll respond.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = str(message.chat.id)
    user_input = message.text

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({"role": "user", "content": user_input})
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=memory[user_id]
    )
    
    reply = response["choices"][0]["message"]["content"]
    
    memory[user_id].append({"role": "assistant", "content": reply})
    save_memory(memory)

    bot.reply_to(message, reply)

bot.polling()
