from flask import Flask, request, jsonify
import os, json
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app

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

    # 建立或附加 token（去重）
    if user_id not in user_tokens:
        user_tokens[user_id] = [fcm_token]
    elif fcm_token not in user_tokens[user_id]:
        user_tokens[user_id].append(fcm_token)

    return jsonify({"message": "Token updated"}), 200

@app.route("/send_notification", methods=["POST"])
def send_notification():
    from firebase_admin import messaging

    data = request.json
    user_id = data.get("user_id")
    title = data.get("title", "通知")
    body = data.get("body", "這是預設訊息")

    tokens = user_tokens.get(user_id)
    if not tokens:
        return jsonify({"error": "User not found or token missing"}), 404

    # 🚧 自動轉換舊格式（單一 string）為 list
    if isinstance(tokens, str):
        tokens = [tokens]
        user_tokens[user_id] = tokens  # 更新為新版格式

    if not tokens:
        return jsonify({"error": "No tokens available"}), 400

    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body),
        tokens=tokens,
    )

    try:
        response = messaging.send_multicast(message)

        # 🔍 移除失敗的 token
        failed_tokens = []
        for idx, resp in enumerate(response.responses):
            if not resp.success:
                failed_tokens.append(tokens[idx])

        if failed_tokens:
            user_tokens[user_id] = [t for t in tokens if t not in failed_tokens]

        return jsonify({
            "message": "Notification sent",
            "success_count": response.success_count,
            "failure_count": response.failure_count,
            "failed_tokens": failed_tokens
        })
    # 新添加print 出來    
    try:
    print(f"🚀 即將推播 tokens: {tokens}")

    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body),
        tokens=tokens,
    )

    response = messaging.send_multicast(message)

    failed_tokens = []
    for idx, resp in enumerate(response.responses):
        if not resp.success:
            failed_tokens.append(tokens[idx])
            print(f"❌ 發送失敗 token: {tokens[idx]} | 原因: {resp.exception}")

    if failed_tokens:
        user_tokens[user_id] = [t for t in tokens if t not in failed_tokens]

    return jsonify({
        "message": "Notification sent",
        "success_count": response.success_count,
        "failure_count": response.failure_count,
        "failed_tokens": failed_tokens
    })

    except Exception as e:
        return jsonify({"error": f"Send failed: {str(e)}"}), 500
        
@app.route("/tokens", methods=["GET"])
def list_tokens():
    return jsonify(user_tokens)
    
