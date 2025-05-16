import os
import requests
import json
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 獲取 API 金鑰
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_KEY")
NEWS_API_KEY = os.getenv("NEWSAPI_KEY")
MOVIE_DB_API_KEY = os.getenv("TMDB_API_KEY")
OWM_API_KEY = os.getenv("OWM_API_KEY")

def check_line_api():
    """檢查 LINE API 連接狀態"""
    print("\n===== 檢查 LINE API =====")
    if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
        print("❌ LINE Bot API 金鑰未設定")
        return False
    
    # 實際上不呼叫 LINE API，只檢查金鑰是否存在
    print("✅ LINE Bot API 金鑰已設定")
    return True

def check_gemini_api():
    """檢查 Google Gemini API 連接狀態"""
    print("\n===== 檢查 Google Gemini API =====")
    if not GEMINI_API_KEY:
        print("❌ Google Gemini API 金鑰未設定")
        return False
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": "Hello, how are you?"}]}
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 100,
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("✅ Google Gemini API 連接成功")
            return True
        else:
            print(f"❌ Google Gemini API 連接失敗，狀態碼: {response.status_code}")
            print(f"錯誤訊息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Google Gemini API 連接失敗: {str(e)}")
        return False

def check_news_api():
    """檢查 NewsAPI 連接狀態"""
    print("\n===== 檢查 NewsAPI =====")
    if not NEWS_API_KEY:
        print("❌ NewsAPI 金鑰未設定")
        return False
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=tw&apiKey={NEWS_API_KEY}&pageSize=1"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✅ NewsAPI 連接成功")
            return True
        else:
            print(f"❌ NewsAPI 連接失敗，狀態碼: {response.status_code}")
            print(f"錯誤訊息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ NewsAPI 連接失敗: {str(e)}")
        return False

def check_tmdb_api():
    """檢查 The Movie Database API 連接狀態"""
    print("\n===== 檢查 TMDb API =====")
    if not MOVIE_DB_API_KEY:
        print("❌ TMDb API 金鑰未設定")
        return False
    
    try:
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={MOVIE_DB_API_KEY}&language=zh-TW&page=1"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✅ TMDb API 連接成功")
            return True
        else:
            print(f"❌ TMDb API 連接失敗，狀態碼: {response.status_code}")
            print(f"錯誤訊息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ TMDb API 連接失敗: {str(e)}")
        return False

def check_owm_api():
    """檢查 OpenWeatherMap API 連接狀態"""
    print("\n===== 檢查 OpenWeatherMap API =====")
    if not OWM_API_KEY:
        print("❌ OpenWeatherMap API 金鑰未設定")
        return False
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Taipei&appid={OWM_API_KEY}&lang=zh_tw&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✅ OpenWeatherMap API 連接成功")
            return True
        else:
            print(f"❌ OpenWeatherMap API 連接失敗，狀態碼: {response.status_code}")
            print(f"錯誤訊息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ OpenWeatherMap API 連接失敗: {str(e)}")
        return False

def main():
    """主函數，執行所有 API 檢查"""
    print("開始檢查 API 連接狀態...")
    
    # 檢查所有 API
    line_status = check_line_api()
    gemini_status = check_gemini_api()
    news_status = check_news_api()
    tmdb_status = check_tmdb_api()
    owm_status = check_owm_api()
    
    # 顯示總結
    print("\n===== API 檢查結果 =====")
    print(f"LINE Bot API: {'✅ 正常' if line_status else '❌ 異常'}")
    print(f"Google Gemini API: {'✅ 正常' if gemini_status else '❌ 異常'}")
    print(f"NewsAPI: {'✅ 正常' if news_status else '❌ 異常'}")
    print(f"TMDb API: {'✅ 正常' if tmdb_status else '❌ 異常'}")
    print(f"OpenWeatherMap API: {'✅ 正常' if owm_status else '❌ 異常'}")
    
    # 總體評估
    if all([line_status, gemini_status, news_status, tmdb_status, owm_status]):
        print("\n✅ 所有 API 連接正常，可以啟動 LINE Bot 服務。")
    else:
        print("\n⚠️ 部分 API 連接異常，可能影響 LINE Bot 功能。")

if __name__ == "__main__":
    main() 