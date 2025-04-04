from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Rasa configuration (default port 5005)
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        # Get user message from request
        data = request.json
        user_message = data.get('message', '')

        # Prepare payload for Rasa
        payload = {
            "sender": "default_user",
            "message": user_message
        }

        # Send to Rasa server
        rasa_response = requests.post(RASA_URL, json=payload)

        # Return bot's response
        if rasa_response.status_code == 200:
            return jsonify(rasa_response.json())
        else:
            return jsonify({"error": "Rasa server unavailable"}), 503

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def chat_interface():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)