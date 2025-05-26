from dotenv import load_dotenv
import os, json
from firebase_admin import credentials, initialize_app

load_dotenv()

# 讀取並解析 JSON
cred_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
cred_dict = json.loads(cred_json)
cred = credentials.Certificate(cred_dict)
initialize_app(cred)
