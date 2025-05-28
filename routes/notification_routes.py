# routes/notification_routes.py
from flask import Blueprint, request, jsonify
from firebase_admin import messaging

notification_bp = Blueprint('notification_bp', __name__)

@notification_bp.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.json
    user_id = data.get("user_id")
    title = data.get("title", "通知")
    body = data.get("body", "這是預設訊息")

    # 假設 user_tokens 是全域變數，實際應從資料庫或其他來源獲取
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
