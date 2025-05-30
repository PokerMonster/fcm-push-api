# routes/multicast_message.py
from flask import Blueprint
import os, json
#import firebase_admin
from firebase_admin import messaging
from dotenv import load_dotenv

multicast_bp = Blueprint('multicast_bp', __name__)

def send_multicast_notification(tokens, title, body, data=None):
    """
    發送推播通知給多個設備。

    :param tokens: List[str] - FCM 註冊 token 列表
    :param title: str - 通知標題
    :param body: str - 通知內容
    :param data: dict - 附加資料（可選）
    :return: dict - 包含成功和失敗的統計資訊與詳細錯誤
    """
    if not tokens:
        return {
            "success_count": 0,
            "failure_count": 0,
            "responses": [],
            "error": "No device tokens provided."
        }

    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
        tokens=tokens,
    )

    try:
        response = messaging.send_multicast(message)
    except Exception as e:
        print(f"發送過程中發生錯誤: {e}")
        return {
            "success_count": 0,
            "failure_count": len(tokens),
            "responses": [],
            "error": str(e)
        }

    detailed_responses = []
    for idx, resp in enumerate(response.responses):
        token = tokens[idx]
        if resp.success:
            print(f"✅ 訊息成功發送至設備 {token}")
            detailed_responses.append({"token": token, "success": True})
        else:
            error_str = str(resp.exception)
            print(f"❌ 發送失敗: {token}, 錯誤：{error_str}")
            detailed_responses.append({
                "token": token,
                "success": False,
                "error": error_str
            })
            # 判斷無效 token
            if "registration token is not a valid FCM token" in error_str or \
               "Requested entity was not found" in error_str or \
               "Unregistered" in error_str:
                invalid_tokens.append(token)

    return {
        "success_count": response.success_count,
        "failure_count": response.failure_count,
        "responses": detailed_responses,
        "invalid_tokens": invalid_tokens
    }
