from flask import Flask, request, abort
import sys
import os

# 添加項目根目錄到路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 導入app實例
from app import app

# Vercel需要的入口點
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) 