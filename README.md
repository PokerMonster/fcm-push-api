.env files 
MYSQL_HOST=ip  
MYSQL_PORT=port  
MYSQL_USER=user  
MYSQL_PASSWORD=password  
MYSQL_DATABASE=db  

FIREBASE_SERVICE_ACCOUNT={"type":"service_account","project_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n", ...}  

======== 
Dockerfile
# Dockerfile  
FROM python:3.11-slim  

# 設定工作目錄  
WORKDIR /app  

# 複製檔案  
COPY . .  

# 安裝系統套件（如 mysqlclient 依賴）  
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev  

# 建立虛擬環境並安裝相依套件  
RUN pip install --upgrade pip  
RUN pip install -r requirements.txt  

# 預設使用 gunicorn 啟動  
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]  
