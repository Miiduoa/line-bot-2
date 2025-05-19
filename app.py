from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, ReplyMessageRequest, TextMessage
import google.generativeai as genai
import requests
import json

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = 'G5/Jatw/Mm7gpHjRnVG89Mxp+6QWXINk4mGkga8o3g9TRa96NXiOed5ylkNZjuUtGHXFKCV46xX1t73PZkYdjlqIFoJHe0XiPUP4EyRy/jwJ6sqRtXivrQNA0WH+DK9pLUKg/ybSZ1mvGywuK8upBAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'ff89f01585f2b68301b8f8911174cd87'

# Google Gemini API 設定
GOOGLE_GEMINI_API_KEY = 'AlzaSyBWCitsjkm7DPe_aREubKIZjqmgXafVKNE'
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

# NewsAPI 設定
NEWS_API_KEY = '5807e3e70bd2424584afdfc6e932108b'
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/top-headlines'

# The Movie Database (TMDb) API 設定
TMDB_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzI4YmU1YzdhNDA1OTczZDdjMjA0NDlkYmVkOTg4OCIsIm5iZiI6MS43NDYwNzg5MDI5MTgwMDAyZSs5LCJzdWIiOiI2ODEzMGNiNjgyODI5Y2NhNzExZmJkNDkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbjoxfQ.FQlIdfWlf4E0Tw9sYRF7txbWymAby77KnHjTVNFSpdM'
TMDB_API_BASE_URL = 'https://api.themoviedb.org/3'

# OpenWeatherMap API 設定
OPENWEATHERMAP_API_KEY = 'CWA-C80C73F3-7042-4D8D-A88A-D39DD2CFF841'
OPENWEATHERMAP_API_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

app = Flask(__name__)

# 設定 LINE Messaging API 用戶端
configuration = Configuration(
    access_token=LINE_CHANNEL_ACCESS_TOKEN
)
line_bot_api = ApiClient(configuration).api

# 設定 Webhook 處理器
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 簡單的上下文記憶體 (userID -> 對話歷史列表)
user_context = {}

def get_news(query):
    """使用 NewsAPI 查詢新聞"""
    params = {
        'q': query,
        'apiKey': NEWS_API_KEY,
        'language': 'zh-TW',  # 設定為繁體中文
        'pageSize': 3       # 限制回傳新聞數量
    }
    try:
        response = requests.get(NEWS_API_ENDPOINT, params=params)
        response.raise_for_status()  # 檢查請求是否成功
        data = response.json()
        if data['status'] == 'ok' and data['totalResults'] > 0:
            news_items = data['articles']
            news_list = []
            for item in news_items:
                title = item['title']
                url = item['url']
                news_list.append(f"標題：{title}\n連結：{url}\n")
            return "\n".join(news_list)
        else:
            return "抱歉，找不到相關新聞。"
    except requests.exceptions.RequestException as e:
        return f"查詢新聞時發生錯誤：{e}"
    except json.JSONDecodeError as e:
        return f"解析新聞資料時發生錯誤：{e}"

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Bot 的 Webhook 接收端點"""
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(message_content_type='text')
def handle_message(event):
    """處理文字訊息"""
    user_id = event.source.user_id
    message_text = event.message.text

    # 取得或初始化使用者的對話歷史
    if user_id not in user_context:
        user_context[user_id] = []

    # 判斷是否為新聞查詢
    if "新聞" in message_text or "最新消息" in message_text:
        query = message_text.replace("新聞", "").replace("最新消息", "").strip()
        if query:
            news_result = get_news(query)
            reply = f"查詢「{query}」的新聞結果如下：\n\n{news_result}"
        else:
            reply = "請問你想查詢什麼關鍵字的新聞呢？"
        messages = [TextMessage(text=reply)]
    else:
        # 將使用者訊息加入對話歷史
        user_context[user_id].append({"role": "user", "parts": [message_text]})

        # 取得 Gemini 的回覆
        try:
            response = gemini_model.generate_content(user_context[user_id])
            gemini_reply = response.text
            user_context[user_id].append({"role": "model", "parts": [gemini_reply]})
            messages = [TextMessage(text=gemini_reply)]
        except Exception as e:
            reply = f"抱歉，Gemini 發生錯誤：{e}"
            messages = [TextMessage(text=reply)]

    # 回覆訊息給使用者
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=messages
        )
    )

@handler.add(message_content_type='group_join')
def handle_group_join(event):
    """處理機器人加入群組事件"""
    reply_message = TextMessage(text="大家好！很高興加入這個群組。請隨時吩咐我查詢新聞、天氣或電影資訊喔！")
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[reply_message]
        )
    )

# 在群組中接收訊息 (需要額外處理，這裡先留空)
@handler.add(message_content_type='text', message_source_type='group')
def handle_group_message(event):
    """處理群組中的文字訊息"""
    # TODO: 將群組訊息加入 Gemini 的上下文
    pass

# 添加根路由以便於健康檢查
@app.route("/")
def home():
    return "LINE Bot is running!"