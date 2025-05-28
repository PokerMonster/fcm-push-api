from flask import Flask, request, jsonify
import os, json
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app

import mysql.connector

db = mysql.connector.connect(
    host=os.environ.get("fcm-mysql-api.in2soft.net:51306"),
    user=os.environ.get("fcmuser"),
    password=os.environ.get("FcMepAss9021"),
    database=os.environ.get("fcmdb")
)
cursor = db.cursor(dictionary=True)

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
    try:
        cursor.execute("""
            INSERT INTO fcm_tokens (user_id, token)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE token = VALUES(token)
        """, (user_id, fcm_token))
        db.commit()
        return jsonify({"message": "Token stored in DB"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
   

@app.route("/send_notification", methods=["POST"])
def send_notification():
    from firebase_admin import messaging

    data = request.json
    user_id = data.get("user_id")
    title = data.get("title", "通知")
    body = data.get("body", "這是預設訊息")

    cursor.execute("SELECT token FROM fcm_tokens WHERE user_id = %s", (user_id,))
    tokens = [row["token"] for row in cursor.fetchall()]
    
    if not tokens:
        return jsonify({"error": "User not found or token missing"}), 404

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        tokens=tokens,
    )

    try:
        response = messaging.send_multicast(message)

        # 自動刪除失敗 token
        for i, r in enumerate(response.responses):
            if not r.success:
                cursor.execute("DELETE FROM fcm_tokens WHERE token = %s", (tokens[i],))
        db.commit()

        return jsonify({
            "message": "Notification sent",
            "success_count": response.success_count,
            "failure_count": response.failure_count
        })
    except Exception as e:
        return jsonify({"error": f"Send failed: {e}"}), 500
        
@app.route("/tokens", methods=["GET"])
def list_tokens():
    return jsonify(user_tokens)
