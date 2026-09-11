import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

def fetch_google_news(limit):
    url = "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=ko&gl=KR&ceid=KR:ko"
    
    try:
        # ⭐️ timeout=5를 주어 5초 안에 응답이 없으면 에러를 뿜도록 안전장치 설정
        response = requests.get(url, timeout=5)
        
        # 만약 인터넷 주소가 잘못되었거나 서버가 고장 났다면(예: 404, 500 에러) 여기서 잡아냅니다.
        response.raise_for_status()
        
    except requests.exceptions.Timeout:
        logging.error("서버 응답 시간이 초과되었습니다. (타임아웃)")
        return []
    except requests.exceptions.RequestException as e:
        logging.error(f"네트워크 오류 발생: {e}")
        return []

    # 정상적으로 가져왔을 때의 처리
    soup = BeautifulSoup(response.text, "xml")
    items = soup.find_all("item")
    
    news_list = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for item in items[:int(limit)]:
        title = item.title.text if item.title else "제목 없음"
        link = item.link.text if item.link else "링크 없음"
        
        news_list.append({
            "제목": title,
            "링크": link,
            "수집시각": now,
            "소스정보": "google_rss",
            "수집방법": "rss",
            "카테고리": "IT"
        })
        
    return news_list