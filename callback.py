from flask import Flask, request
import sys
import os

# 將專案根目錄加入路徑，使 import 能正常運作
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 導入 app 實例
from app import app as flask_app

# 這是 Vercel 用來處理請求的函數
def handler(request):
    # 將 Vercel 的請求轉換為 Flask 能處理的請求
    with flask_app.request_context(request):
        return flask_app.full_dispatch_request()

# Vercel 部署時會尋找 handler 函數
handler = lambda req: handler(req) 