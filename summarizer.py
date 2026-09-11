def summarize_news(title):
    """
    뉴스 제목을 바탕으로 AI 요약문을 생성하는 함수입니다.
    (실제 API 키 연결 시 이 부분에서 외부 AI API를 호출합니다)
    """
    # 간단한 핵심 요약문 생성 (테스트용)
    summary = f"[AI 요약] '{title}' 관련 주요 IT 트렌드 이슈입니다."
    return summary

def process_summaries(news_list, option="unsummarized"):
    summarized_count = 0
    
    for news in news_list:
        # 이미 요약된 뉴스인지 확인
        already_done = "요약" in news and news["요약"] != ""
        
        # --unsummarized 옵션일 때 이미 요약된 건 스킵
        if option == "unsummarized" and already_done:
            continue
            
        # 요약 생성
        news["요약"] = summarize_news(news["제목"])
        news["상태"] = "summarized"
        summarized_count += 1
        
    return news_list, summarized_count