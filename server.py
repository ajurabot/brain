from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Allow frontend communication

# Load backend URL from config
def get_backend_url():
    with open("config.json", "r") as file:
        return json.load(file)["backend_url"]

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Ajura AI Backend is Running!"})

# Handle incoming messages
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get("message", "")
    
    if message.startswith("ajura4498"):
        # Route to ChatGPT for real-time responses
        response = {"response": f"ChatGPT Answer: {message}"}
    else:
        # Future Ajura AI responses will be handled here
        response = {"response": f"Ajura AI is processing: {message}"}
    
    return jsonify(response)

# Webhook for secret updates
@app.route('/api/webhook', methods=['POST'])
def webhook():
    auth_key = request.headers.get("Authorization")
    
    if auth_key != os.getenv("SECRET_WEBHOOK", "default-key"):
        return jsonify({"error": "Unauthorized"}), 403

    update_data = request.json
    return jsonify({"status": "Update received", "data": update_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
