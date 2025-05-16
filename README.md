# LINE Bot 多功能助手

一個具備天氣查詢、電影資訊、新聞摘要和 AI 聊天功能的 LINE Bot。

## 功能

- **天氣查詢**：使用 OpenWeatherMap API 查詢城市天氣
- **電影資訊**：使用 TMDb API 搜尋電影詳情
- **新聞摘要**：透過 NewsAPI 獲取最新新聞
- **智能對話**：使用 Google Gemini AI 進行對話

## 環境準備

1. 建立虛擬環境並安裝套件

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. 設定環境變數（可創建 `.env` 檔案並使用 `python-dotenv` 載入）

```
CHANNEL_ACCESS_TOKEN=你的LINE_Channel_Access_Token
CHANNEL_SECRET=你的LINE_Channel_Secret
GOOGLE_GEMINI_KEY=你的Google_Gemini_API_Key
NEWSAPI_KEY=你的NewsAPI_Key
TMDB_API_KEY=你的TMDb_API_Key
OWM_API_KEY=你的OpenWeatherMap_API_Key
```

## 啟動服務

### 本地開發

```bash
python app.py
```

服務會在 http://localhost:5000 啟動，但需要外部可訪問的 URL 用於 LINE Webhook。

可使用 ngrok 等工具建立臨時公開連結：
```bash
ngrok http 5000
```

### Vercel 部署

此專案已配置為可直接部署至 Vercel。專案結構如下：

```
my_line_bot/
├── api/
│   └── callback.py   # Flask 應用程式入口點
├── requirements.txt  # 相依套件
└── vercel.json       # Vercel 配置
```

部署步驟：

1. 註冊 [Vercel](https://vercel.com/) 帳號並安裝 Vercel CLI
   ```bash
   npm i -g vercel
   ```

2. 登入 Vercel
   ```bash
   vercel login
   ```

3. 在專案目錄執行部署
   ```bash
   vercel
   ```

4. 部署完成後，將 Vercel 提供的網址加上 `/callback` 路徑設定為 LINE Bot 的 Webhook URL
   例如：`https://your-app-name.vercel.app/callback`

## 使用方法

- **天氣查詢**：`天氣 台北`
- **電影資訊**：`電影 蜘蛛人`
- **新聞摘要**：`新聞`
- **一般對話**：直接輸入文字即可與 AI 聊天 