def clean_data(raw_news_list):
    clean_list = []
    seen_links = set() # 중복인지 확인하기 위한 마법의 기억장치

    for news in raw_news_list:
        # 1. 중복 기사 거르기 (skip 정책 적용)
        # 만약 이미 저장한 링크라면, 이 기사는 버리고 다음 기사로 넘어갑니다.
        if news["링크"] in seen_links:
            continue 
        
        seen_links.add(news["링크"]) # 처음 보는 링크면 기억장치에 등록!

        # 2. 텍스트 정제 (제목 앞뒤의 쓸데없는 띄어쓰기 지우기)
        clean_title = news["제목"].strip()

        # 3. 깨끗해진 기사 포장하기
        clean_news = {
            "제목": clean_title,
            "링크": news["링크"],
            "수집시각": news["수집시각"],
            "상태": "cleaned" # ⭐️ 정제되었다는 새로운 꼬리표 달기!
        }
        clean_list.append(clean_news)

    return clean_list