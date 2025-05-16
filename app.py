import os
import json
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LINE Bot settings
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
MOVIE_DB_API_KEY = os.getenv("MOVIE_DB_API_KEY") 
OWM_API_KEY = os.getenv("OWM_API_KEY")

app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Store conversation context (for development; use Redis or DB in production)
conversation_context = {}

@app.route("/", methods=["GET"])
def index():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    
    # Get user or group ID for context tracking
    if event.source.type == 'group':
        context_id = event.source.group_id
    elif event.source.type == 'room':
        context_id = event.source.room_id
    else:
        context_id = event.source.user_id

    # Initialize context if needed
    if context_id not in conversation_context:
        conversation_context[context_id] = []
    conversation_context[context_id].append({"role": "user", "content": user_text})

    reply = None
    # Weather query
    if '天氣' in user_text:
        reply = get_weather(user_text)
    # News query
    elif '新聞' in user_text:
        reply = get_news()
    # Movie query
    elif '電影' in user_text:
        reply = get_movies(user_text)
    # Flirting feature
    elif any(keyword in user_text for keyword in ['哈囉', '妳', '你', '在嗎']):
        reply = flirt(event, context_id)
    # Default: Generate response using Gemini
    else:
        reply = chat_with_gemini(context_id)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    
    # Get user or group ID for context tracking
    if event.source.type == 'group':
        context_id = event.source.group_id
    elif event.source.type == 'room':
        context_id = event.source.room_id
    else:
        context_id = event.source.user_id
        
    # Initialize context if needed
    if context_id not in conversation_context:
        conversation_context[context_id] = []
    
    reply = None
    
    if data == 'action=weather':
        reply = "請輸入想查詢的城市天氣，例如：「台北天氣」"
    elif data == 'action=news':
        reply = get_news()
    elif data == 'action=movies':
        reply = get_movies("")
    elif data == 'action=chat':
        reply = "您好！有什麼我可以幫助您的？"
    elif data == 'action=about':
        reply = "我是一個多功能LINE機器人，可以查詢天氣、新聞、電影，並且能和您聊天。"
    elif data == 'action=help':
        reply = "使用說明：\n- 輸入「台北天氣」查詢台北天氣\n- 輸入「新聞」獲取最新新聞\n- 輸入「電影」獲取熱門電影推薦\n- 輸入任何文字和我聊天"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

# Weather API call
def get_weather(text):
    city = extract_city(text) or 'Taipei'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&lang=zh_tw&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        res = response.json()
        
        desc = res['weather'][0]['description']
        temp = res['main']['temp']
        humidity = res['main']['humidity']
        feels_like = res['main']['feels_like']
        
        return f"{city} 現在天氣：{desc}，氣溫 {temp}°C，體感溫度 {feels_like}°C，濕度 {humidity}%"
    except Exception as e:
        return f"抱歉，無法取得天氣資訊：{str(e)}"

def extract_city(text):
    # Common cities in Taiwan and China
    cities = ['台北', '臺北', 'Taipei', '高雄', '台中', '臺中', '台南', '臺南', '新竹', 
              '花蓮', '宜蘭', '彰化', '嘉義', '屏東', '苗栗', '南投', '雲林', '基隆', 
              '桃園', '新北', '金門', '澎湖', '馬祖', '北京', '上海', '廣州', '深圳']
    
    for city in cities:
        if city in text:
            return city
    return None

# News API call
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=tw&apiKey={NEWS_API_KEY}&pageSize=5"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        res = response.json()
        
        articles = res.get('articles', [])
        if not articles:
            return "抱歉，目前無法取得最新新聞"
            
        msg = '今日新聞：\n'
        for art in articles:
            msg += f"- {art['title']} ({art['source']['name']})\n"
        return msg
    except Exception as e:
        return f"抱歉，無法取得新聞資訊：{str(e)}"

# Movie API call
def get_movies(text):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={MOVIE_DB_API_KEY}&language=zh-TW&page=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        res = response.json()
        
        results = res.get('results', [])[:5]
        if not results:
            return "抱歉，目前無法取得電影資訊"
            
        msg = '熱門電影：\n'
        for m in results:
            msg += f"- {m['title']}，評分 {m['vote_average']}\n"
        return msg
    except Exception as e:
        return f"抱歉，無法取得電影資訊：{str(e)}"

# Flirting dialog
def flirt(event, context_id):
    return chat_with_gemini(context_id, system_prompt="你是一個風趣幽默的聊天助手，可以進行輕鬆的閒聊。請用繁體中文回覆，答案簡短有趣。")

# Interact with Gemini
def chat_with_gemini(context_id, system_prompt=None):
    try:
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "parts": [{"text": system_prompt}]})
        
        # Convert conversation context to Gemini format
        for msg in conversation_context[context_id][-10:]:
            role = "user" if msg["role"] == "user" else "model"
            messages.append({"role": role, "parts": [{"text": msg["content"]}]})
        
        payload = {
            "contents": messages,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 800,
            }
        }
        
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        
        if "candidates" in result and result["candidates"]:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            conversation_context[context_id].append({"role": "assistant", "content": reply})
            return reply
        else:
            return "抱歉，我現在無法回應，請稍後再試。"
    except Exception as e:
        return f"與AI對話發生錯誤：{str(e)}"

# For Vercel deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True) 