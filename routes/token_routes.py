# routes/token_routes.py
from flask import Blueprint, request, jsonify

token_bp = Blueprint('token_bp', __name__)

user_tokens = {}

@token_bp.route('/update_token', methods=['POST'])
def update_token():
    data = request.json
    user_id = data.get("user_id")
    fcm_token = data.get("fcm_token")
    if not user_id or not fcm_token:
        return jsonify({"error": "Missing user_id or fcm_token"}), 400
    user_tokens[user_id] = fcm_token
    return jsonify({"message": "Token updated"}), 200

@token_bp.route('/tokens', methods=['GET'])
def list_tokens():
    return jsonify(user_tokens)
