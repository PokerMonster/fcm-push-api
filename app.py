from dotenv import load_dotenv
import os, json
from firebase_admin import credentials, initialize_app

load_dotenv()

# 讀取並解析 JSON
raw = os.environ.get("FIREBASE_SERVICE_ACCOUNT")

# 先轉成字典
cred_dict = json.loads(raw)

# 還原換行符號：把 "\\n" 換成 "\n"
cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

# 用 firebase_admin 初始化
cred = credentials.Certificate(cred_dict)
initialize_app(cred)
