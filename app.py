import os
import json
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage,
    QuickReply, QuickReplyButton, MessageAction, RichMenu, RichMenuArea,
    RichMenuBounds, RichMenuSize, PostbackAction, URIAction
)
from dotenv import load_dotenv
import flex_templates

# 載入環境變數
load_dotenv()

# 設定 LINE Bot 權杖與密鑰
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN", "G5/Jatw/Mm7gpHjRnVG89Mxp+6QWXINk4mGkga8o3g9TRa96NXiOed5ylkNZjuUtGHXFKCV46xX1t73PZkYdjlqIFoJHe0XiPUP4EyRy/jwJ6sqRtXivrQNA0WH+DK9pLUKg/ybSZ1mvGywuK8upBAdB04t89/1O/w1O/w1cDnyilFU=")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET", "ff89f01585f2b68301b8f8911174cd87")

# 設定第三方 API 金鑰
GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_KEY", "AlzaSyBWCitsjkm7DPe_aREubKIZjqmgXafVKNE")
NEWS_API_KEY = os.getenv("NEWSAPI_KEY", "5807e3e70bd2424584afdfc6e932108b")
MOVIE_DB_API_KEY = os.getenv("TMDB_API_KEY", "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzI4YmU1YzdhNDA1OTczZDdjMjA0NDlkYmVkOTg4OCIsIm5iZiI6MS43NDYwNzg5MDI5MTgwMDAyYSs5LCJzdWIiOiI2ODEzMGNiNjgyODI5Y2NhNzExZmJkNDkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.FQlIdfWlf4E0Tw9sYRF7txbWymAby77KnHjTVNFSpdM")
OWM_API_KEY = os.getenv("OWM_API_KEY", "CWA-C80C73F3-7042-4D8D-A88A-D39DD2CFF841")

app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 儲存群組對話脈絡與最近查詢紀錄 (測試用，生產可換 Redis 或資料庫)
conversation_context = {}
recent_cities = {}

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route('/setup', methods=['GET'])
def setup_rich_menu():
    """設置 Rich Menu"""
    try:
        # 刪除現有的 Rich Menu
        rich_menu_list = line_bot_api.get_rich_menu_list()
        for rich_menu in rich_menu_list:
            line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)
        
        # 建立新的 Rich Menu
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=2500, height=1686),
            selected=True,
            name="功能選單",
            chat_bar_text="功能選單",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                    action=MessageAction(label='天氣查詢', text='天氣 台北')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                    action=MessageAction(label='電影資訊', text='電影')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
                    action=MessageAction(label='新聞摘要', text='新聞')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=843, width=1250, height=843),
                    action=MessageAction(label='AI 對話', text='你好，請問你是誰？')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1250, y=843, width=1250, height=843),
                    action=MessageAction(label='使用說明', text='使用說明')
                )
            ]
        )
        
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        
        # 上傳 Rich Menu 圖片
        # 這裡應該上傳一個實際的圖片，但這只是示例，所以只返回 ID
        # 實際應用中，可以使用 PIL 或其他庫生成圖片，或者上傳預先準備好的圖片
        
        # 設定為預設選單
        line_bot_api.set_default_rich_menu(rich_menu_id)
        
        return f"Rich Menu 創建成功! ID: {rich_menu_id}"
    except Exception as e:
        return f"設置 Rich Menu 時發生錯誤: {str(e)}"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    
    # 取得用戶或群組ID
    if hasattr(event.source, 'group_id'):
        chat_id = event.source.group_id
    elif hasattr(event.source, 'user_id'):
        chat_id = event.source.user_id
    else:
        chat_id = 'default'

    # 初始化脈絡
    if chat_id not in conversation_context:
        conversation_context[chat_id] = []
    conversation_context[chat_id].append({"role": "user", "content": user_text})

    try:
        # 使用說明
        if '使用說明' in user_text:
            reply = get_help_message()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )
            return
            
        # 天氣查詢
        if '天氣' in user_text:
            weather_info = get_weather(user_text, chat_id)
            line_bot_api.reply_message(
                event.reply_token,
                weather_info
            )
            return
            
        # 新聞查詢
        elif '新聞' in user_text:
            news_info = get_news()
            line_bot_api.reply_message(
                event.reply_token,
                news_info
            )
            return
            
        # 電影查詢
        elif '電影' in user_text:
            movie_info = get_movies(user_text)
            line_bot_api.reply_message(
                event.reply_token,
                movie_info
            )
            return
            
        # 搭訕功能
        elif any(keyword in user_text for keyword in ['哈囉', '妳', '你', '在嗎']):
            reply = flirt(chat_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )
            return
            
        # 預設：交給 Gemini 生成回應
        else:
            reply = chat_with_gemini(chat_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )
            return
            
    except Exception as e:
        # 錯誤處理
        error_message = f"抱歉，處理訊息時發生錯誤: {str(e)}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=error_message)
        )

def get_help_message():
    """產生使用說明訊息"""
    return """📚 使用說明

🌦️ 天氣查詢：輸入「天氣 城市名」
例如：天氣 台北

🎬 電影資訊：
- 輸入「電影」查看熱門電影
- 輸入「電影 電影名」搜尋特定電影
例如：電影 蜘蛛人

📰 新聞摘要：輸入「新聞」獲取今日熱門新聞

💬 一般對話：直接輸入文字與 AI 聊天

你也可以透過下方的功能選單快速選擇功能！"""

# 天氣 API 呼叫
def get_weather(text, chat_id):
    # 解析地點
    city = 'Taipei'  # 預設為台北
    
    # 從文本中提取城市名稱
    words = text.split()
    for i, word in enumerate(words):
        if word == '天氣' and i < len(words) - 1:
            city = words[i+1]
            break
    
    # 記錄最近查詢的城市
    if chat_id not in recent_cities:
        recent_cities[chat_id] = []
    
    if city not in recent_cities[chat_id]:
        recent_cities[chat_id].insert(0, city)
        recent_cities[chat_id] = recent_cities[chat_id][:3]  # 只保留最近三個
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&lang=zh_tw&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return TextSendMessage(text=f"無法獲取 {city} 的天氣資訊，請確認城市名稱是否正確。")
            
        weather_data = response.json()
        
        # 創建天氣 Flex Message
        flex_message = FlexSendMessage.new_from_json_dict(
            flex_templates.get_weather_flex(city, weather_data)
        )
        
        # 添加快速回覆按鈕（最近查詢的城市）
        quick_reply_buttons = []
        for recent_city in recent_cities[chat_id]:
            if recent_city != city:  # 不顯示當前城市
                quick_reply_buttons.append(
                    QuickReplyButton(
                        action=MessageAction(label=f"{recent_city}天氣", text=f"天氣 {recent_city}")
                    )
                )
        
        if quick_reply_buttons:
            flex_message.quickReply = QuickReply(items=quick_reply_buttons)
            
        return flex_message
        
    except Exception as e:
        return TextSendMessage(text=f"查詢天氣時發生錯誤：{str(e)}")

# 新聞 API 呼叫
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=tw&apiKey={NEWS_API_KEY}&pageSize=5"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return TextSendMessage(text="無法獲取新聞資訊，請稍後再試。")
            
        res = response.json()
        articles = res.get('articles', [])
        
        if not articles:
            return TextSendMessage(text="目前沒有可顯示的新聞。")
        
        # 使用 Flex Message 模板顯示新聞
        flex_message = FlexSendMessage.new_from_json_dict(
            flex_templates.get_news_flex(articles)
        )
        
        return flex_message
        
    except Exception as e:
        return TextSendMessage(text=f"查詢新聞時發生錯誤：{str(e)}")

# 電影 API 呼叫
def get_movies(text):
    # 檢查是否有特定電影名稱
    movie_name = None
    words = text.split()
    for i, word in enumerate(words):
        if word == '電影' and i < len(words) - 1:
            movie_name = words[i+1]
            break
    
    try:
        if movie_name:
            # 搜尋特定電影
            url = f"https://api.themoviedb.org/3/search/movie?api_key={MOVIE_DB_API_KEY}&language=zh-TW&query={movie_name}&page=1"
            response = requests.get(url)
            if response.status_code != 200:
                return TextSendMessage(text="無法搜尋電影資訊，請稍後再試。")
                
            res = response.json()
            results = res.get('results', [])
            
            if not results:
                return TextSendMessage(text=f"找不到與 '{movie_name}' 相關的電影。")
            
            # 返回第一個最相關的電影的 Flex Message
            flex_message = FlexSendMessage.new_from_json_dict(
                flex_templates.get_movie_flex(results[0])
            )
            
            return flex_message
            
        else:
            # 獲取熱門電影
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={MOVIE_DB_API_KEY}&language=zh-TW&page=1"
            response = requests.get(url)
            if response.status_code != 200:
                return TextSendMessage(text="無法獲取電影資訊，請稍後再試。")
                
            res = response.json()
            results = res.get('results', [])[:5]
            
            if not results:
                return TextSendMessage(text="目前沒有可顯示的熱門電影。")
            
            # 只顯示第一部熱門電影的詳細資訊，如果需要顯示多部，可以使用 Carousel 模式
            flex_message = FlexSendMessage.new_from_json_dict(
                flex_templates.get_movie_flex(results[0])
            )
            
            return flex_message
            
    except Exception as e:
        return TextSendMessage(text=f"查詢電影時發生錯誤：{str(e)}")

# 搭訕對話
def flirt(chat_id):
    # 使用 Gemini 生成幽默搭訕
    return chat_with_gemini(chat_id, system_prompt="你是一個幽默風趣的對話助手，請以友好、有趣的方式回應用戶的問候。")

# 與 Gemini 互動
def chat_with_gemini(chat_id, system_prompt=None):
    try:
        # Google Gemini API 有不同的端點和參數結構
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {
            'Content-Type': 'application/json'
        }
        
        # 添加 API key 作為查詢參數
        url = f"{url}?key={GEMINI_API_KEY}"
        
        # 準備對話內容
        context = []
        if system_prompt:
            context.append({"role": "system", "parts": [{"text": system_prompt}]})
        
        # 添加最近 10 條對話記錄
        for msg in conversation_context[chat_id][-10:]:
            role = "user" if msg["role"] == "user" else "model"
            context.append({"role": role, "parts": [{"text": msg["content"]}]})
        
        # 準備請求數據
        payload = {
            "contents": context,
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 800,
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            return f"AI 回應出錯 (狀態碼: {response.status_code})，請稍後再試。"
        
        res = response.json()
        
        # 從回應中提取文本
        if "candidates" in res and res["candidates"]:
            reply = res["candidates"][0]["content"]["parts"][0]["text"]
            # 保存回應到對話上下文
            conversation_context[chat_id].append({"role": "assistant", "content": reply})
            return reply
        else:
            return "AI 無法生成回應，請稍後再試。"
            
    except Exception as e:
        return f"與 AI 對話時發生錯誤：{str(e)}"

@app.route('/')
def index():
    return "LINE Bot is running! 訪問 /setup 以設置 Rich Menu。"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True) 