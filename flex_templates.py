"""
LINE Bot 的 Flex Message 模板

此檔案包含預先定義的 Flex Message 模板，用於增強訊息的視覺呈現效果。
"""

def get_weather_flex(city, weather_data):
    """
    生成天氣資訊的 Flex Message
    
    Args:
        city (str): 城市名稱
        weather_data (dict): 天氣資料字典
    
    Returns:
        dict: Flex Message 格式的天氣資訊
    """
    # 獲取天氣圖標的URL
    icon_code = weather_data['weather'][0]['icon']
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    
    # 獲取天氣詳情
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    description = weather_data['weather'][0]['description']
    
    return {
        "type": "flex",
        "altText": f"{city} 天氣資訊",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{city} 天氣資訊",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#ffffff"
                    }
                ],
                "backgroundColor": "#27ACB2"
            },
            "hero": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "url": icon_url,
                        "size": "full",
                        "aspectRatio": "1:1",
                        "aspectMode": "fit"
                    },
                    {
                        "type": "text",
                        "text": description,
                        "align": "center",
                        "weight": "bold",
                        "size": "xl"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "溫度",
                                "weight": "bold",
                                "size": "md",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": f"{temp}°C",
                                "size": "md",
                                "align": "end",
                                "flex": 1
                            }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "體感溫度",
                                "weight": "bold",
                                "size": "md",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": f"{feels_like}°C",
                                "size": "md",
                                "align": "end",
                                "flex": 1
                            }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "濕度",
                                "weight": "bold",
                                "size": "md",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": f"{humidity}%",
                                "size": "md",
                                "align": "end",
                                "flex": 1
                            }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "風速",
                                "weight": "bold",
                                "size": "md",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": f"{wind_speed} m/s",
                                "size": "md",
                                "align": "end",
                                "flex": 1
                            }
                        ],
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "資料來源: OpenWeatherMap",
                        "size": "xs",
                        "color": "#aaaaaa",
                        "align": "center"
                    }
                ]
            }
        }
    }

def get_movie_flex(movie_data):
    """
    生成電影資訊的 Flex Message
    
    Args:
        movie_data (dict): 電影資料字典
    
    Returns:
        dict: Flex Message 格式的電影資訊
    """
    # 獲取電影海報URL（如果有）
    poster_path = movie_data.get('poster_path')
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
    
    # 獲取電影詳情
    title = movie_data.get('title', '無標題')
    vote = movie_data.get('vote_average', 'N/A')
    release_date = movie_data.get('release_date', '未知日期')
    overview = movie_data.get('overview', '無簡介')
    
    # 截短簡介
    if overview and len(overview) > 100:
        overview = overview[:100] + "..."
    
    return {
        "type": "flex",
        "altText": f"電影資訊: {title}",
        "contents": {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": poster_url,
                "size": "full",
                "aspectRatio": "2:3",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "xl",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "icon",
                                "size": "sm",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                            },
                            {
                                "type": "text",
                                "text": f"{vote}/10",
                                "size": "sm",
                                "color": "#999999",
                                "margin": "md"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "上映日期",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": release_date,
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 5
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "contents": [
                            {
                                "type": "text",
                                "text": "簡介",
                                "weight": "bold",
                                "size": "md"
                            },
                            {
                                "type": "text",
                                "text": overview,
                                "wrap": True,
                                "margin": "sm"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "資料來源: TMDb",
                        "size": "xs",
                        "color": "#aaaaaa",
                        "align": "center"
                    }
                ]
            }
        }
    }

def get_news_flex(articles):
    """
    生成新聞摘要的 Flex Message
    
    Args:
        articles (list): 新聞文章列表
    
    Returns:
        dict: Flex Message 格式的新聞摘要
    """
    # 創建新聞卡片列表
    contents = []
    
    # 最多顯示 5 條新聞
    for article in articles[:5]:
        title = article.get('title', '無標題')
        source = article.get('source', {}).get('name', '未知來源')
        url = article.get('url', '')
        published_at = article.get('publishedAt', '').split('T')[0]  # 只取日期部分
        
        # 獲取新聞圖片（如果有）
        image_url = article.get('urlToImage')
        if not image_url:
            image_url = "https://via.placeholder.com/580x300?text=No+Image"
        
        # 創建新聞卡片
        news_bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": image_url,
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "md",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": source,
                                "size": "sm",
                                "color": "#999999",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": published_at,
                                "size": "sm",
                                "color": "#999999",
                                "align": "end"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "閱讀更多",
                            "uri": url
                        }
                    }
                ]
            }
        }
        
        contents.append(news_bubble)
    
    return {
        "type": "flex",
        "altText": "今日新聞摘要",
        "contents": {
            "type": "carousel",
            "contents": contents
        }
    } 