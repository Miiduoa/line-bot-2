# LINE 聊天機器人

這是一個整合了多種 API 的 LINE 聊天機器人，包括天氣、新聞、電影資訊和 AI 對話功能。

## 功能

1. **天氣查詢**: 輸入包含"天氣"關鍵字的訊息
2. **新聞查詢**: 輸入包含"新聞"關鍵字的訊息
3. **電影查詢**: 輸入包含"電影"關鍵字的訊息
4. **搭訕功能**: 輸入包含"哈囉"、"你"、"妳"、"在嗎"等關鍵字的訊息
5. **AI 對話**: 其他訊息將自動透過 Gemini API 生成回應

## 部署到 Vercel

### 事前準備

1. 在 [LINE Developers](https://developers.line.biz/) 建立一個 Channel
2. 在 [Vercel](https://vercel.com/) 建立帳號

### 部署步驟

1. 將此專案 clone 到本地，或直接在 Vercel 上導入:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. 安裝 Vercel CLI (如果你想在本地部署):

```bash
npm install -g vercel
```

3. 透過 Vercel CLI 部署:

```bash
vercel
```

或者直接在 Vercel 儀表板上導入 GitHub 專案。

4. 部署完成後，你會得到一個 URL (例如 `https://your-project.vercel.app`)

5. 回到 LINE Developers 主控台，將 Webhook URL 設定為:

```
https://your-project.vercel.app/callback
```

6. 確保 LINE Channel 的 "Use webhook" 設定已啟用

### Webhook 重要說明

根據 LINE 官方文檔，webhook 處理有以下重要要點：

1. **異步處理事件**: 我們已實現異步處理以避免延遲後續事件的處理
2. **簽名驗證**: 使用 x-line-signature 頭部進行簽名驗證，而非 IP 位址驗證
3. **狀態碼回應**: 接收到 LINE Platform 的 HTTP POST 請求後必須立即返回 200 狀態碼
4. **控制台監控**: 如果仍有問題，請在 LINE Developers Console 查看 webhook 狀態

## 環境變數

建議將所有 API 金鑰設置為環境變數。在 Vercel 儀表板中可以設定以下環境變數:

- `CHANNEL_ACCESS_TOKEN`: LINE Bot 的 Channel Access Token
- `CHANNEL_SECRET`: LINE Bot 的 Channel Secret
- `GEMINI_API_KEY`: Google Gemini API 金鑰
- `NEWS_API_KEY`: News API 金鑰
- `MOVIE_DB_API_KEY`: The Movie DB API 金鑰
- `OWM_API_KEY`: OpenWeatherMap API 金鑰

## 本地開發

1. 安裝依賴:

```bash
pip install -r requirements.txt
```

2. 運行應用:

```bash
python api/index.py
```

3. 使用工具如 ngrok 建立臨時公開網址:

```bash
ngrok http 3000
```

4. 將 ngrok 提供的 URL 加上 `/callback` 作為 LINE Bot Webhook URL

### 測試 Webhook

在設置好 webhook URL 後，你可以在 LINE Developers Console 中點擊 "Verify" 按鈕來測試連接。如果看到成功消息，表示你的 webhook 設置正確 