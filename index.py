import os
import json
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設定 LINE Bot 權杖與密鑰
CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN', "G5/Jatw/Mm7gpHjRnVG89Mxp+6QWXINk4mGkga8o3g9TRa96NXiOed5ylkNZjuUtGHXFKCV46xX1t73PZkYdjlqIFoJHe0XiPUP4EyRy/jwJ6sqRtXivrQNA0WH+DK9pLUKg/ybSZ1mvGywuK8upBAdB04t89/1O/w1O/w1cDnyilFU=")
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET', "ff89f01585f2b68301b8f8911174cd87")

# 設定第三方 API 金鑰
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', "AlzaSyBWCitsjkm7DPe_aREubKIZjqmgXafVKNE")
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', "5807e3e70bd2424584afdfc6e932108b")
MOVIE_DB_API_KEY = os.environ.get('MOVIE_DB_API_KEY', "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzI4YmU1YzdhNDA1OTczZDdjMjA0NDlkYmVkOTg4OCIsIm5iZiI6MS43NDYwNzg5MDI5MTgwMDAyYSs5LCJzdWIiOiI2ODEzMGNiNjgyODI5Y2NhNzExZmJkNDkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.FQlIdfWlf4E0Tw9sYRF7txbWymAby77KnHjTVNFSpdM")
OWM_API_KEY = os.environ.get('OWM_API_KEY', "CWA-C80C73F3-7042-4D8D-A88A-D39DD2CFF841")

app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 儲存群組對話脈絡 (測試用，生產可換 Redis 或資料庫)
conversation_context = {}

@app.route("/api/callback", methods=["POST"])
def api_callback():
    return process_webhook()

@app.route("/callback", methods=["POST"])
def callback():
    return process_webhook()

def process_webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running!"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    group_id = event.source.group_id if hasattr(event.source, 'group_id') else event.source.user_id

    # 初始化脈絡
    if group_id not in conversation_context:
        conversation_context[group_id] = []
    conversation_context[group_id].append({"role": "user", "content": user_text})

    reply = None
    # 天氣查詢
    if '天氣' in user_text:
        reply = get_weather(user_text)
    # 新聞查詢
    elif '新聞' in user_text:
        reply = get_news()
    # 電影查詢
    elif '電影' in user_text:
        reply = get_movies(user_text)
    # 搭訕功能
    elif any(keyword in user_text for keyword in ['哈囉', '妳', '你', '在嗎']):
        reply = flirt(event, group_id)
    # 預設：交給 Gemini 生成回應
    else:
        reply = chat_with_gemini(group_id)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

# 天氣 API 呼叫
def get_weather(text):
    # 解析地點
    city = 'Taipei'
    # TODO: 從 text 擷取城市
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&lang=zh_tw&units=metric"
    res = requests.get(url).json()
    desc = res['weather'][0]['description']
    temp = res['main']['temp']
    return f"{city} 現在天氣：{desc}，氣溫 {temp}°C"

# 新聞 API 呼叫
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=tw&apiKey={NEWS_API_KEY}&pageSize=5"
    res = requests.get(url).json()
    articles = res.get('articles', [])
    msg = '今日新聞：\n'
    for art in articles:
        msg += f"- {art['title']} ({art['source']['name']})\n"
    return msg

# 電影 API 呼叫
def get_movies(text):
    # 解析電影名稱或熱門
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={MOVIE_DB_API_KEY}&language=zh-TW&page=1"
    res = requests.get(url).json()
    results = res.get('results', [])[:5]
    msg = '熱門電影：\n'
    for m in results:
        msg += f"- {m['title']}，評分 {m['vote_average']}\n"
    return msg

# 搭訕對話
def flirt(event, group_id):
    # 使用 Gemini 生成幽默搭訕
    return chat_with_gemini(group_id, system_prompt="You are a witty flirting assistant.")

# 與 Gemini 互動
def chat_with_gemini(group_id, system_prompt=None):
    payload = {
        'model': 'chat-bison-001',
        'messages': []
    }
    if system_prompt:
        payload['messages'].append({'role': 'system', 'content': system_prompt})
    for msg in conversation_context[group_id][-10:]:
        payload['messages'].append(msg)
    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json'
    }
    try:
        res = requests.post('https://gemini.googleapis.com/v1/chat/completions',
                            headers=headers, data=json.dumps(payload)).json()
        reply = res['choices'][0]['message']['content']
        conversation_context[group_id].append({'role': 'assistant', 'content': reply})
        return reply
    except Exception as e:
        return f"Sorry, I'm having trouble connecting to my AI services. Error: {str(e)}"

# 入口點用於本地測試
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
    
# Vercel 需要的處理函式
def handler(event, context):
    return app 