# routes/multicast_message.py
from flask import Blueprint
import os, json
#import firebase_admin
from firebase_admin import messaging
from dotenv import load_dotenv

multicast_bp = Blueprint('multicast_bp', __name__)

def send_multicast_notification(tokens, title, body, data=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
        tokens=tokens,
    )

    try:
        response = messaging.send_multicast(message)
    except Exception as e:
        print(f"发送通知时发生错误: {e}")
        return {
            "success_count": 0,
            "failure_count": len(tokens),
            "responses": [],
            "error": str(e)
        }

    if not tokens:
        print("设备令牌列表为空，无法发送通知。")
        return {
            "success_count": 0,
            "failure_count": 0,
            "responses": [],
            "error": "No device tokens provided."
        }

    for idx, resp in enumerate(response.responses):
        if resp.success:
            print(f"訊息成功發送至設備 {tokens[idx]}")
        else:
            print(f"訊息發送至設備 {tokens[idx]} 失敗，錯誤：{resp.exception}")
    return {
        "success_count": response.success_count,
        "failure_count": response.failure_count,
        "responses": [r.__dict__ for r in response.responses],
    }
