from flask import Flask
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

@app.route("/")
def index():
    return "✅ Flask + Firebase Ready on Render!"
