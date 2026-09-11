import matplotlib.pyplot as plt
import os

def generate_report(news_list, insights):
    news_count = len(news_list)
    # 1. 📊 그래프 그리기 (시각화)
    # 맥북에서 한글이 깨지지 않게 'AppleGothic' 폰트를 설정해 줍니다.
    plt.rcParams['font.family'] = 'AppleGothic'
    plt.rcParams['axes.unicode_minus'] = False
    
    # x축(이름)과 y축(숫자) 데이터 준비
    category_counts = {}

    for news in news_list:
        category = news.get("카테고리", "IT")
        category_counts[category] = category_counts.get(category, 0) + 1

    categories = list(category_counts.keys())
    counts = list(category_counts.values())
    
    # 막대그래프 그리기
    plt.figure(figsize=(6, 4))
    plt.bar(categories, counts, color='skyblue', linewidth=0)
    plt.title("카테고리별 뉴스 수")
    plt.ylabel("뉴스 개수")
    
    # 그린 그래프를 이미지 파일(PNG)로 저장!
    plt.savefig("news_chart.png")
    plt.close()

    # 2. 📈 일자별 수집 추이 그래프 만들기
    daily_counts = {}

    for news in news_list:
        collected_at = news.get("수집시각", "")

        if collected_at:
            date = collected_at.split(" ")[0]
            daily_counts[date] = daily_counts.get(date, 0) + 1

    dates = list(daily_counts.keys())
    counts_by_date = list(daily_counts.values())

    plt.figure(figsize=(8, 4))
    plt.plot(dates, counts_by_date, marker="o")
    plt.title("일자별 뉴스 수집 추이")
    plt.xlabel("수집 날짜")
    plt.ylabel("뉴스 개수")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("news_daily_trend.png")
    plt.close()

    # 품질 지표 계산
    summarized_count = sum(
        1 for news in news_list
        if news.get("상태") == "summarized"
    )

    if news_count > 0:
        summary_rate = summarized_count / news_count * 100
    else:
        summary_rate = 0

    required_fields = ["제목", "링크", "수집시각"]

    complete_count = sum(
        1 for news in news_list
        if all(news.get(field) for field in required_fields)
    )

    if news_count > 0:
        completeness_rate = complete_count / news_count * 100
    else:
        completeness_rate = 0

    # TOP N 집계
    top_categories = sorted(
        category_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]
    
    # 3. 📝 최종 텍스트 보고서(MD) 만들기
    report_text = f"""# 📊 AI 뉴스 트렌드 종합 리포트

    ## 1. 데이터 수집 통계
    - **총 수집된 뉴스 기사:** {news_count}건
    - **요약 완료된 뉴스:** {summarized_count}건 ({summary_rate:.2f}%)
    - **완료된 뉴스:** {complete_count}건 ({completeness_rate:.2f}%)
    - **분석 상태:** 요약 및 트렌드 분석 완료
    """
    report_text += "\n## 2. 카테고리 TOP 3\n"

    for rank, (category, count) in enumerate(top_categories, start=1):
        report_text += f"{rank}. **{category}** - {count}건\n"

    report_text += "\n## 3. 🤖 AI 인사이트 분석 결과\n"
    report_text += "\n### 📈 주요 트렌드\n"

    # 트렌드 목록을 하나씩 꺼내서 보고서에 덧붙이기
    for trend in insights["주요_트렌드"]:
        report_text += f"- {trend}\n"
        
    report_text += f"\n### 🔑 핵심 키워드\n{', '.join(insights['핵심_키워드'])}\n"
    report_text += f"\n### 💡 시사점\n{insights['시사점']}\n"
    
    # 완성된 텍스트를 파일로 저장!
    with open("final_report.md", "w", encoding="utf-8") as file:
        file.write(report_text)