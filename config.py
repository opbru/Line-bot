import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class Config:
    """應用程式設定"""

    # LINE Bot 設定
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

    # Flask 設定
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

    # 資料庫設定
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///accounting.db')

    # 靜態檔案設定
    STATIC_URL = os.getenv('STATIC_URL', 'http://localhost:5000/static')
    UPLOAD_FOLDER = 'static/charts'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # 其他設定
    TIMEZONE = 'Asia/Taipei'