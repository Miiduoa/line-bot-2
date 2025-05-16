# LINE Bot 聊天機器人

這是一個多功能的 LINE 聊天機器人，可以提供天氣查詢、新聞資訊、電影推薦和聊天功能。

## 功能

1. **天氣查詢** - 輸入城市名稱和「天氣」關鍵字即可查詢目前天氣
2. **新聞查詢** - 輸入「新聞」即可獲取最新新聞
3. **電影推薦** - 輸入「電影」獲取熱門電影推薦
4. **聊天功能** - 使用 Google Gemini 提供智能對話功能

## 安裝與設定

### 前置需求

- Python 3.7+
- LINE 開發者帳號
- 各 API 服務的金鑰
- Vercel 帳號 (用於部署)

### 本地開發步驟

1. 安裝依賴套件：

```bash
pip install -r requirements.txt
```

2. 設定環境變數：

複製 `.env.example` 為 `.env` 並填入您的 API 金鑰：

```
# LINE Bot API Keys
LINE_CHANNEL_ACCESS_TOKEN=你的LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET=你的LINE_CHANNEL_SECRET

# Third-party API Keys
GEMINI_API_KEY=你的GEMINI_API_KEY
NEWS_API_KEY=你的NEWS_API_KEY
MOVIE_DB_API_KEY=你的MOVIE_DB_API_KEY
OWM_API_KEY=你的OWM_API_KEY
```

3. 啟動伺服器：

```bash
python app.py
```

4. 使用 ngrok 等工具將本地伺服器暴露到網際網路：

```bash
ngrok http 3000
```

5. 將 ngrok 提供的 HTTPS URL + `/callback` 設定為 LINE 開發者控制台的 Webhook URL。

## 部署到 Vercel

1. 首先安裝 Vercel CLI：

```bash
npm install -g vercel
```

2. 登入 Vercel：

```bash
vercel login
```

3. 部署專案：

```bash
vercel
```

4. 設定環境變數：在 Vercel 網站後台的專案設定中，添加所有 API 金鑰作為環境變數。

5. 將 Vercel 提供的 URL + `/callback` 設定為 LINE 開發者控制台的 Webhook URL。

## 使用說明

- 輸入「台北天氣」查詢台北天氣
- 輸入「新聞」獲取最新新聞
- 輸入「電影」獲取熱門電影推薦
- 輸入任何其他文字進行聊天

## LICENSE

MIT 