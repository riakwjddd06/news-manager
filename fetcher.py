import requests
from bs4 import BeautifulSoup
from datetime import datetime # ⭐️ 지금 몇 시인지 알려주는 도구 추가!

def fetch_google_news(limit):
    url = "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=ko&gl=KR&ceid=KR:ko"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml")
    items = soup.find_all("item")
    
    news_list = []
    
    # ⭐️ 지금 이 순간의 날짜와 시간을 만들어냅니다. (예: 2026-09-11 12:15:53)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for item in items[:int(limit)]:
        title = item.title.text
        link = item.link.text
        
        # ⭐️ 미션 요구사항에 맞춰 꼬리표 3개를 추가했습니다!
        news_list.append({
            "제목": title,
            "링크": link,
            "수집시각": now,           # 언제?
            "소스정보": "google_rss",  # 어디서?
            "수집방법": "rss"          # 어떻게?
        })
        
    return news_list