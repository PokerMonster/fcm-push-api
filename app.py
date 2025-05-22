from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

user_tokens = {}

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
    data = request.json
    user_id = data.get("user_id")
    title = data.get("title")
    body = data.get("body")

    token = user_tokens.get(user_id)
    if not token:
        return jsonify({"error": "User not found or no token"}), 404

    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
    )

    try:
        response = messaging.send(message)
        return jsonify({"message": "Notification sent", "id": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
