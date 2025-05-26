import os
import json
from firebase_admin import credentials, initialize_app

# 從環境變數讀取 JSON 內容
firebase_key_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")

if not firebase_key_json:
    raise Exception("Missing FIREBASE_SERVICE_ACCOUNT environment variable")

cred_dict = json.loads(firebase_key_json)
cred = credentials.Certificate(cred_dict)
initialize_app(cred)
