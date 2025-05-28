# multicast_message.py
from flask import Blueprint
import os, json
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv

multicast_bp = Blueprint('multicast_bp', __name__)

load_dotenv()
# 初始化 Firebase Admin SDK
cred_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
cred_dict = json.loads(cred_json)
cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
cred = credentials.Certificate(cred_dict)
initialize_app(cred)

def send_multicast_notification(tokens, title, body, data=None):
    """
    發送推播通知給多個設備。

    :param tokens: List[str] - FCM 註冊 token 列表
    :param title: str - 通知標題
    :param body: str - 通知內容
    :param data: dict - 附加資料（可選）
    :return: dict - 包含成功和失敗的統計資訊
    """
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
        tokens=tokens,
    )

    response = messaging.send_multicast(message)
    return {
        "success_count": response.success_count,
        "failure_count": response.failure_count,
        "responses": [r.__dict__ for r in response.responses],
    }
