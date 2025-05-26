from flask import Flask, request, jsonify
import os, json
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app

load_dotenv()

cred_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
cred_dict = json.loads(cred_json)
cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
cred = credentials.Certificate(cred_dict)
initialize_app(cred)

app = Flask(__name__)  # ← 必須是 app！
user_tokens = {}

@app.route("/")
def index():
    return "✅ Flask + Firebase Ready on Render!"
    
@app.route("/update_token", methods=["POST"])
def update_token():
    data = request.json
    user_id = data.get("user_id")
    fcm_token = data.get("fcm_token")
    if not user_id or not fcm_token:
        return jsonify({"error": "Missing user_id or fcm_token"}), 400
    user_tokens[user_id] = fcm_token
    return jsonify({"message": "Token updated"}), 200

@app.route("/send_notification", methods=["POST"])
def send_notification():
    from firebase_admin import messaging

    data = request.json
    user_id = data.get("user_id")
    title = data.get("title", "通知")
    body = data.get("body", "這是預設訊息")

    token = user_tokens.get(user_id)
    if not token:
        return jsonify({"error": "User not found or token missing"}), 404

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    try:
        response = messaging.send(message)
        return jsonify({"message": "Notification sent", "id": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route("/tokens", methods=["GET"])
def list_tokens():
    return jsonify(user_tokens)
    
