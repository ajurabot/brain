from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend connections

# Hidden webhook (change this before deployment)
SECRET_WEBHOOK = os.getenv("AJURA_SECRET_WEBHOOK", "your-secret-key")

@app.route("/", methods=["GET"])
def home():
    return "Ajura AI Backend is running!"

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("text", "")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Simulated AI response (Replace this with real AI logic)
    ai_response = f"Ajura received: {user_message}"

    return jsonify({"response": ai_response})

# Webhook for hidden updates (secured with a secret key)
@app.route("/api/webhook", methods=["POST"])
def webhook():
    auth_key = request.headers.get("Authorization")
    
    if auth_key != SECRET_WEBHOOK:
        return jsonify({"error": "Unauthorized"}), 403
    
    update_data = request.json
    # Process updates here (e.g., deploy new model, change settings)
    
    return jsonify({"status": "Update received", "data": update_data})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
