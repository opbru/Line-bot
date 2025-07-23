# LINE Bot 記帳小幫手

一個使用 LINE Bot 的智慧記帳助手，讓您透過簡單的對話就能記錄日常支出，並提供統計分析功能。

## 功能特色

### 核心功能
- 📝 **快速記帳**：輸入「類別 金額」即可記錄支出
- 🔍 **查詢記錄**：查看最近 5 筆支出記錄
- 🗑️ **刪除功能**：刪除錯誤的記錄
- 📊 **週統計**：查看本週各類別支出統計與圖表
- 🤖 **智慧分類**：自動識別常見支出類別

### 支援的類別
- 飲食（早餐、午餐、晚餐、飲料等）
- 交通（捷運、公車、計程車等）
- 購物、娛樂、生活、醫療、教育

## 測試方式

### 1. 加入 LINE Bot 好友
掃描 QR Code 或搜尋 Bot ID 加入好友

### 2. 基本指令測試

#### 查看使用說明
```
說明
```

#### 新增支出
```
早餐 65
午餐 120 牛肉麵
交通 30
```

#### 查詢最近記錄
```
查帳
```

#### 刪除記錄
```
刪除第1筆
```

#### 查看週統計
```
本週總結
```

### 3. 測試流程建議
1. 先輸入「說明」了解所有功能
2. 記錄幾筆不同類別的支出
3. 使用「查帳」確認記錄正確
4. 嘗試「本週總結」查看統計
5. 測試「刪除」功能

## Webhook 架設與 LINE Bot 設定

### 1. LINE Developers Console 設定

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 建立新的 Provider（或使用現有的）
3. 建立新的 Messaging API Channel
4. 取得以下資訊：
   - **Channel Secret**（Basic settings 頁面）
   - **Channel Access Token**（Messaging API 頁面，點擊 Issue）

### 2. Webhook 設定

#### 本地開發（使用 ngrok）
```bash
# 啟動應用程式
python app.py

# 另開終端機，使用 ngrok 建立公開 URL
ngrok http 5000

# 將 ngrok 提供的 https URL 設定到 LINE Console
# 例如：https://xxxxx.ngrok.io/callback
```

#### 生產環境（Railway）
1. 部署到 Railway 後取得公開 URL
2. 在 LINE Console 設定 Webhook URL：
   ```
   https://your-app-name.up.railway.app/callback
   ```

### 3. LINE Console 必要設定
- **Webhook URL**：設定為 `你的網址/callback`
- **Use webhook**：開啟
- **Auto-reply messages**：關閉
- **Greeting messages**：可選

## 資料庫 Schema

### Users 表（使用者）
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | Integer (PK) | 使用者 ID |
| line_user_id | String(50) | LINE 使用者 ID |
| display_name | String(100) | 顯示名稱 |
| created_at | DateTime | 建立時間 |

### Expenses 表（支出記錄）
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | Integer (PK) | 記錄 ID |
| user_id | Integer (FK) | 使用者 ID |
| category | String(50) | 支出類別 |
| amount | Float | 金額 |
| description | String(200) | 備註說明 |
| created_at | DateTime | 建立時間 |

### 關聯設計
- 一個使用者可以有多筆支出記錄（一對多關係）
- 使用 `line_user_id` 作為識別使用者的唯一值
- 刪除使用者時會連帶刪除其所有支出記錄

## 部署架構說明

### 使用平台：Railway

Railway 是一個現代化的雲端部署平台，提供簡單的 Git 整合部署。

### 系統架構

```
使用者 <-> LINE App <-> LINE Platform
              |
              v
        Webhook (HTTPS)
              |
              v
    Railway App (Flask Server)
              |
              v
        PostgreSQL DB
```

### 技術堆疊
- **後端框架**：Python Flask
- **LINE SDK**：line-bot-sdk-python
- **資料庫**：
  - 開發環境：SQLite
  - 生產環境：PostgreSQL (Railway 提供)
- **ORM**：SQLAlchemy
- **Web Server**：Gunicorn
- **圖表生成**：QuickChart API

### 部署設定

#### 環境變數
在 Railway Variables 中設定：
- `LINE_CHANNEL_ACCESS_TOKEN`：LINE Channel Access Token
- `LINE_CHANNEL_SECRET`：LINE Channel Secret
- `DATABASE_URL`：自動由 Railway 提供

#### 自動部署流程
1. 推送程式碼到 GitHub
2. Railway 自動觸發部署
3. 執行 `pip install -r requirements.txt`
4. 使用 Gunicorn 啟動服務

### 擴展性考量
- 使用 PostgreSQL 支援並發請求
- 無狀態設計，可水平擴展
- 圖表使用外部 API，減少伺服器負載

## 本地開發設定

### 1. 環境需求
- Python 3.8+
- pip
- ngrok（用於測試 webhook）

### 2. 安裝步驟
```bash
# 克隆專案
git clone <repository-url>
cd linebot-accounting

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝相依套件
pip install -r requirements.txt
```

### 3. 環境變數設定
建立 `.env` 檔案：
```env
LINE_CHANNEL_ACCESS_TOKEN=你的_Channel_Access_Token
LINE_CHANNEL_SECRET=你的_Channel_Secret
FLASK_ENV=development
DATABASE_URL=sqlite:///accounting.db
STATIC_URL=https://your-domain.com/static
```

### 4. 執行應用程式
```bash
python app.py
```

## 專案結構
```
linebot-accounting/
├── app.py                 # 主程式進入點
├── config.py             # 設定檔
├── requirements.txt      # Python 套件清單
├── bot/                  # LINE Bot 相關模組
│   ├── handlers.py      # 訊息處理器
│   └── flex_messages.py # Flex Message 模板
├── database/            # 資料庫相關
│   ├── models.py       # 資料模型
│   └── db_manager.py   # 資料庫操作
└── utils/              # 工具模組
    ├── text_parser.py  # 文字解析器
    ├── category_classifier.py # 類別分類器
    └── chart_generator.py # 圖表生成器
```

## 未來優化方向

- [ ] 加入月統計與年統計功能
- [ ] 支援預算設定與提醒
- [ ] 實作趨勢分析圖表
- [ ] 加入匯出功能（CSV/PDF）
- [ ] 開發 LIFF 網頁介面
- [ ] 支援多種貨幣

## 授權

MIT License