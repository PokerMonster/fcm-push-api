# routes/notification_routes.py
from flask import Blueprint, request, jsonify
from firebase_admin import messaging
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

notification_bp = Blueprint('notification_bp', __name__)

@notification_bp.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.json
    user_id = data.get("user_id")
    title = data.get("title", "通知")
    body = data.get("body", "這是預設訊息")

    # 假設 user_tokens 是全域變數，實際應從資料庫或其他來源獲取
    try:
        db = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            port=int(os.environ.get("MYSQL_PORT")),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE")
        )
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT token FROM fcm_tokens WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()

        if not result:
            return jsonify({"error": "User not found or token missing"}), 404

        token = result['token']

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )

        response = messaging.send(message)
        return jsonify({"message": "Notification sent", "id": response})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
