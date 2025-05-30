
import json
import os
from flask import Blueprint, request, jsonify
from google.oauth2 import service_account
import google.auth.transport.requests
import requests

send_direct_bp = Blueprint('send_direct_bp', __name__)

# 讀取 Firebase Admin SDK JSON（從環境變數 FIREBASE_SERVICE_ACCOUNT）
cred_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
if not cred_json:
    raise RuntimeError("FIREBASE_SERVICE_ACCOUNT 環境變數未設置")

cred_dict = json.loads(cred_json)
credentials = service_account.Credentials.from_service_account_info(
    cred_dict,
    scopes=["https://www.googleapis.com/auth/firebase.messaging"]
)
project_id = cred_dict.get("project_id")
if not project_id:
    raise RuntimeError("Firebase service account JSON 缺少 project_id")

def get_access_token():
    request_auth = google.auth.transport.requests.Request()
    credentials.refresh(request_auth)
    return credentials.token

@send_direct_bp.route('/send_direct_fcm', methods=['POST'])
def send_direct_fcm():
    data = request.get_json()
    token = data.get("token")
    title = data.get("title", "測試通知")
    body = data.get("body", "這是直接發送的 FCM 通知")

    if not token:
        return jsonify({"error": "缺少 token"}), 400

    access_token = get_access_token()
    url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }

    message = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    response = requests.post(url, headers=headers, json=message)
    if response.status_code == 200:
        return jsonify({"message": "✅ 發送成功", "response": response.json()})
    else:
        return jsonify({
            "error": "❌ 發送失敗",
            "status_code": response.status_code,
            "response": response.text
        }), 500
