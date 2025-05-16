import os
import argparse
from linebot import LineBotApi
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import io

# 載入環境變數
load_dotenv()

# 取得 LINE Bot API 金鑰
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")

def create_rich_menu_image():
    """生成 Rich Menu 的背景圖片"""
    print("開始生成 Rich Menu 圖片...")
    
    # 創建一個 2500x1686 大小的圖片
    width, height = 2500, 1686
    half_width, half_height = width // 2, height // 2
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 繪製網格線（區域邊界）
    draw.line([(833, 0), (833, 843)], fill=(200, 200, 200), width=2)  # 第一列垂直線
    draw.line([(1666, 0), (1666, 843)], fill=(200, 200, 200), width=2)  # 第二列垂直線
    draw.line([(0, 843), (width, 843)], fill=(200, 200, 200), width=2)  # 水平線
    draw.line([(1250, 843), (1250, height)], fill=(200, 200, 200), width=2)  # 第二行垂直線
    
    # 添加顏色和標籤
    # 天氣區域
    draw.rectangle([(0, 0), (833, 843)], fill=(135, 206, 235), outline=(200, 200, 200), width=2)
    # 電影區域
    draw.rectangle([(833, 0), (1666, 843)], fill=(255, 175, 175), outline=(200, 200, 200), width=2)
    # 新聞區域
    draw.rectangle([(1666, 0), (width, 843)], fill=(152, 251, 152), outline=(200, 200, 200), width=2)
    # AI 對話區域
    draw.rectangle([(0, 843), (1250, height)], fill=(230, 230, 250), outline=(200, 200, 200), width=2)
    # 使用說明區域
    draw.rectangle([(1250, 843), (width, height)], fill=(255, 228, 181), outline=(200, 200, 200), width=2)
    
    # 嘗試加載字體（如果可用）
    try:
        font = ImageFont.truetype("Arial.ttf", 80)
    except IOError:
        # 如果無法加載特定字體，使用默認字體
        font = ImageFont.load_default()
    
    # 添加文字
    draw.text((416, 421), "天氣查詢", fill=(0, 0, 0), font=font)
    draw.text((1249, 421), "電影資訊", fill=(0, 0, 0), font=font)
    draw.text((2082, 421), "新聞摘要", fill=(0, 0, 0), font=font)
    draw.text((625, 1264), "AI 對話", fill=(0, 0, 0), font=font)
    draw.text((1875, 1264), "使用說明", fill=(0, 0, 0), font=font)
    
    # 保存圖片
    image_path = "rich_menu.png"
    image.save(image_path)
    print(f"Rich Menu 圖片已保存為 {image_path}")
    return image_path

def upload_rich_menu_image(rich_menu_id, image_path):
    """上傳 Rich Menu 圖片"""
    print(f"上傳 Rich Menu 圖片至 ID: {rich_menu_id}")
    
    try:
        with open(image_path, 'rb') as f:
            line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
            line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)
        print("Rich Menu 圖片上傳成功！")
        return True
    except Exception as e:
        print(f"上傳 Rich Menu 圖片時發生錯誤: {e}")
        return False

def validate_env_vars():
    """驗證需要的環境變數是否已設定"""
    required_vars = [
        "CHANNEL_ACCESS_TOKEN", 
        "CHANNEL_SECRET", 
        "GOOGLE_GEMINI_KEY", 
        "NEWSAPI_KEY", 
        "TMDB_API_KEY", 
        "OWM_API_KEY"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"警告: 缺少以下環境變數:")
        for var in missing:
            print(f"  - {var}")
        print("請在 .env 檔案中設定這些變數，或直接設定系統環境變數。")
        return False
    
    print("所有必要的環境變數皆已設定。")
    return True

def main():
    parser = argparse.ArgumentParser(description='LINE Bot 設置工具')
    parser.add_argument('--create-rich-menu', action='store_true', help='生成 Rich Menu 圖片')
    parser.add_argument('--validate-env', action='store_true', help='驗證環境變數')
    parser.add_argument('--rich-menu-id', type=str, help='上傳圖片至特定 Rich Menu ID')
    args = parser.parse_args()
    
    if args.validate_env:
        validate_env_vars()
    
    if args.create_rich_menu:
        image_path = create_rich_menu_image()
        if args.rich_menu_id:
            upload_rich_menu_image(args.rich_menu_id, image_path)
    
    if not any([args.validate_env, args.create_rich_menu]):
        parser.print_help()

if __name__ == "__main__":
    main() 