import mysql.connector
from dotenv import load_dotenv

def mysql_module():
    data = request.get_json()
    user_id = data.get("user_id")
    title = data.get("title", "通知")
    body = data.get("body", "這是預設訊息")

    try:
        # 建立資料庫連線
        db = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            port=int(os.environ.get("MYSQL_PORT")),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE")
        )
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT token FROM fcm_tokens WHERE user_id = %s", (user_id,))
        results = cursor.fetchall()
        cursor.close()
        db.close()
