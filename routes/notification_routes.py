# routes/notification_routes.py
from flask import Blueprint, request, jsonify
from firebase_admin import messaging
import mysql.connector
import os
from dotenv import load_dotenv
from .multicast_message import send_multicast_notification
from module.db import get_db_connection

load_dotenv()

notification_bp = Blueprint('notification_bp', __name__)

@notification_bp.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_id = data.get("user_id")
    title = data.get("title", "通知")
    body = data.get("body", "這是預設訊息")

    try:
        db = get_db_connection()
        if db:     
            cursor = db.cursor(buffered=True, dictionary=True)
            cursor.execute("SELECT token FROM fcm_tokens WHERE user_id = %s", (user_id,))
            results = cursor.fetchall()
            cursor.close()
            db.close()

            if not results:
                return jsonify({"error": "User not found or token missing"}), 404

            tokens = [row['token'] for row in results]
            response = send_multicast_notification(tokens, title, body)

            # optional log details
            for idx, r in enumerate(response.get("responses", [])):
                if r.get("success"):
                    print(f"✅ 成功發送至: {tokens[idx]}")
                else:
                    print(f"❌ 發送失敗: {tokens[idx]}, 錯誤：{r.get('error')}")

            return jsonify(response)
        else:
            return jsonify({"error": "Database connection failed"}), 500
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
