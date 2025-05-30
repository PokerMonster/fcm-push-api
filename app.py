from flask import Flask, request, jsonify
import os, json
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app
import mysql.connector
from routes.token_routes import token_bp
from routes.notification_routes import notification_bp
from routes.send_direct_fcm import send_direct_bp

load_dotenv()

cred_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
cred_dict = json.loads(cred_json)
cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
cred = credentials.Certificate(cred_dict)
initialize_app(cred)

app = Flask(__name__)  # ← 必須是 app！
user_tokens = {}
app.register_blueprint(token_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(send_direct_bp)


db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT')),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

# 建立数据库连接
try:
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    print("✅ 成功连接到数据库")
except mysql.connector.Error as err:
    print(f"❌ 数据库连接失败: {err}")


@app.route("/")
def index():
    return "✅ Flask + Firebase Ready on Render!"

if __name__ == "__main__":
    app.run()
    
