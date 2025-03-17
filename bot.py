from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Fetching Telegram Bot Token from Render Environment Variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Ensure this is set correctly in Render

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    print("Received Update:", update)  # Debugging: Logs incoming updates

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Send a test response to verify webhook functionality
        response_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": f"You said: {text}"}
        
        response = requests.post(response_url, json=payload)
        print("Response Status:", response.status_code, response.json())  # Log response

    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
