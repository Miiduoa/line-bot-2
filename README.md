# LINE 聊天機器人

這是一個簡單的LINE聊天機器人專案，可以部署到Vercel。

## 功能

- 回應文字訊息
- 回應圖片、影片、音訊和貼圖
- 自動回覆常見問候語

## 前置需求

1. 一個 [LINE Developer帳號](https://developers.line.biz/)
2. 一個 [Vercel帳號](https://vercel.com/)
3. Node.js 14.0.0 或更高版本

## 設定流程

### LINE 開發者設定

1. 登入 [LINE Developer Console](https://developers.line.biz/console/)
2. 建立一個新的 Provider（若沒有）
3. 建立一個新的 Messaging API 頻道
4. 記下 `Channel Secret` 和 `Channel Access Token`（將在後續步驟中使用）

### 本地開發

1. 安裝相依套件：
   ```bash
   npm install
   ```

2. 在專案根目錄建立 `.env.local` 檔案，加入以下內容（替換為你的實際資訊）：
   ```
   LINE_CHANNEL_ACCESS_TOKEN=你的頻道存取權杖
   LINE_CHANNEL_SECRET=你的頻道密鑰
   ```

3. 本地啟動服務：
   ```bash
   npm run dev
   ```

4. 使用 [ngrok](https://ngrok.com/) 或類似工具建立公開 URL（用於開發測試）：
   ```bash
   ngrok http 3000
   ```

5. 將產生的 URL + `/webhook` 設定為 LINE 開發者控制台中的 Webhook URL
   例如：`https://your-ngrok-url.ngrok.io/webhook`

### Vercel 部署

1. 使用 [Vercel CLI](https://vercel.com/cli) 部署：
   ```bash
   npm install -g vercel
   vercel login
   vercel
   ```

2. 或者，將專案推送到 GitHub 並從 Vercel 儀表板連接存儲庫。

3. 在 Vercel 儀表板上設定環境變數：
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_CHANNEL_SECRET`

4. 部署完成後，將 Vercel 生成的 URL + `/webhook` 設定為 LINE 開發者控制台中的 Webhook URL
   例如：`https://your-app.vercel.app/webhook`

5. 確保在 LINE 開發者控制台中啟用 Webhook

## 自訂和擴展

你可以修改 `api/index.js` 檔案來自訂機器人的行為：

- `handleEvent` 函數處理文字訊息
- `handleNonTextContent` 函數處理非文字訊息（圖片、影片等）

## 提示

- 確保在開發測試期間 Webhook 的 URL 是 HTTPS
- 部署後請在 LINE 官方帳號設定頁面打開 Webhook
- 測試機器人前記得先將官方帳號加為好友 