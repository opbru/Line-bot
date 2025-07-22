import os
import sys
from flask import Flask, request, abort, send_from_directory
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

from config import Config
from bot.handlers import MessageHandler

# 建立 Flask app
app = Flask(__name__)
app.config.from_object(Config)

# 建立上傳資料夾
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化 LINE Bot
line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['LINE_CHANNEL_SECRET'])

# 初始化訊息處理器
message_handler = MessageHandler(line_bot_api)

@app.route("/")
def index():
    """首頁"""
    return """
    <h1>LINE Bot 記帳小幫手</h1>
    <p>Webhook URL: /callback</p>
    <p>Status: Running</p>
    """

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Bot Webhook 端點"""
    # 取得 X-Line-Signature header 值
    signature = request.headers['X-Line-Signature']

    # 取得 request body 作為文字
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 驗證簽章並處理請求
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """處理文字訊息事件"""
    message_handler.handle_text_message(event)

@app.route('/static/<path:filename>')
def static_files(filename):
    """提供靜態檔案"""
    return send_from_directory('static', filename)

@app.errorhandler(Exception)
def handle_error(error):
    """全域錯誤處理"""
    app.logger.error(f"Unhandled exception: {error}")
    return "Internal Server Error", 500

if __name__ == "__main__":
    # 開發環境設定
    port = int(os.environ.get('PORT', 5000))

    # 確認必要的環境變數
    if not app.config['LINE_CHANNEL_ACCESS_TOKEN'] or not app.config['LINE_CHANNEL_SECRET']:
        print("請設定 LINE_CHANNEL_ACCESS_TOKEN 和 LINE_CHANNEL_SECRET 環境變數")
        sys.exit(1)

    print(f"Starting LINE Bot server on port {port}...")
    print(f"Webhook URL: http://localhost:{port}/callback")
    print("請使用 ngrok 建立公開 URL 並設定到 LINE Developer Console")

    app.run(host='0.0.0.0', port=port, debug=app.config['FLASK_DEBUG'])