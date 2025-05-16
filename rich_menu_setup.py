import os
import json
import requests
from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize, PostbackAction
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LINE Bot settings
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def create_rich_menu():
    # Create rich menu object
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=1686),
        selected=True,
        name="LineBot功能選單",
        chat_bar_text="點擊開啟選單",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                action=PostbackAction(label='天氣查詢', data='action=weather')
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                action=PostbackAction(label='新聞查詢', data='action=news')
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
                action=PostbackAction(label='電影推薦', data='action=movies')
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=843, width=833, height=843),
                action=PostbackAction(label='聊天', data='action=chat')
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=833, y=843, width=833, height=843),
                action=PostbackAction(label='關於', data='action=about')
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1666, y=843, width=833, height=843),
                action=PostbackAction(label='幫助', data='action=help')
            )
        ]
    )
    
    # Create rich menu
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    print(f"Rich menu created with ID: {rich_menu_id}")
    
    # Upload rich menu image
    with open('rich_menu.jpg', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, 'image/jpeg', f)
    
    # Set default rich menu
    line_bot_api.set_default_rich_menu(rich_menu_id)
    print("Rich menu set as default")
    
    return rich_menu_id

if __name__ == "__main__":
    try:
        rich_menu_id = create_rich_menu()
        print(f"Rich menu setup complete. ID: {rich_menu_id}")
    except Exception as e:
        print(f"Error setting up rich menu: {str(e)}") 