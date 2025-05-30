# routes/token_routes.py
from flask import Blueprint, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
from module.db import get_db_connection


load_dotenv()
token_bp = Blueprint('token_bp', __name__)

user_tokens = {}

@token_bp.route('/update_token', methods=['POST'])
def update_token():
    data = request.json
    user_id = data.get("user_id")
    fcm_token = data.get("fcm_token")
    if not user_id or not fcm_token:
        return jsonify({"error": "Missing user_id or fcm_token"}), 400

    db = get_db_connection()
    if db:
        cursor = db.cursor()
        # 使用 INSERT ... ON DUPLICATE KEY UPDATE 语句来插入或更新 token
        cursor.execute("""
            INSERT INTO fcm_tokens (user_id, token)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE token = VALUES(token)
        """, (user_id, fcm_token))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Token updated"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@token_bp.route('/tokens', methods=['GET'])
def list_tokens():
    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT user_id, token FROM fcm_tokens")
        tokens = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(tokens)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
