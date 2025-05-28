# routes/notification_routes.py
from flask import Blueprint, request, jsonify
from firebase_admin import messaging
import mysql.connector
import os
from dotenv import load_dotenv
from .multicast_message import send_multicast_notification

load_dotenv()

notification_bp = Blueprint('notification_bp', __name__)

@notification_bp.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_id = data.get("user_id")
    title = data.get("title", "通知")
    body = data.get("body", "這是預設訊息")

    try:
        # 建立資料庫連線
        db = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            port=int(os.environ.get("MYSQL_PORT")),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE")
        )
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT token FROM fcm_tokens WHERE user_id = %s", (user_id,))
        results = cursor.fetchall()
        cursor.close()
        db.close()

        if not result:
            return jsonify({"error": "User not found or token missing"}), 404

        tokens = [row['token'] for row in results]
        response = send_multicast_notification(tokens, title, body)

        return jsonify({
            "message": "Notification sent",
            "success": response["success_count"],
            "failure": response["failure_count"]
        })
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
