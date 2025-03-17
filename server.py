import os
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load Telegram bot token from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Ensure this is set in Render

# Logging for debugging
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET"])
def home():
    """Check if the server is running"""
    return "Ajura AI is Live!", 200

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    """Handles Telegram webhook updates dynamically"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        logging.info(f"Received Telegram update: {data}")
        
        # Extract message details (optional)
        chat_id = data.get("message", {}).get("chat", {}).get("id")
        text = data.get("message", {}).get("text")

        if chat_id and text:
            logging.info(f"Message from {chat_id}: {text}")

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is not set in environment variables!")
    
    app.run(host="0.0.0.0", port=10000)
