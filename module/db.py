# db.py
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT')),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

def get_db_connection():
    try:
        db = mysql.connector.connect(**db_config)
        print("✅ 成功连接到数据库")
        return db
    except mysql.connector.Error as err:
        print(f"❌ 数据库连接失败: {err}")
        return None
