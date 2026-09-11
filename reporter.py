import matplotlib.pyplot as plt
import os

def generate_report(news_count, insights):
    # 1. 📊 그래프 그리기 (시각화)
    # 맥북에서 한글이 깨지지 않게 'AppleGothic' 폰트를 설정해 줍니다.
    plt.rcParams['font.family'] = 'AppleGothic'
    plt.rcParams['axes.unicode_minus'] = False
    
    # x축(이름)과 y축(숫자) 데이터 준비
    categories = ['IT / 과학 뉴스']
    counts = [news_count]
    
    # 막대그래프 그리기
    plt.figure(figsize=(6, 4))
    plt.bar(categories, counts, color='skyblue')
    plt.title("오늘의 뉴스 수집 현황")
    plt.ylabel("뉴스 개수")
    
    # 그린 그래프를 이미지 파일(PNG)로 저장!
    plt.savefig("news_chart.png")
    plt.close()
    
    # 2. 📝 최종 텍스트 보고서(MD) 만들기
    report_text = f"""# 📊 AI 뉴스 트렌드 종합 리포트

## 1. 데이터 수집 통계
- **총 수집된 뉴스 기사:** {news_count}건
- **분석 상태:** 요약 및 트렌드 분석 완료

## 2. 🤖 AI 인사이트 분석 결과

### 📈 주요 트렌드
"""
    # 트렌드 목록을 하나씩 꺼내서 보고서에 덧붙이기
    for trend in insights["주요_트렌드"]:
        report_text += f"- {trend}\n"
        
    report_text += f"\n### 🔑 핵심 키워드\n{', '.join(insights['핵심_키워드'])}\n"
    report_text += f"\n### 💡 시사점\n{insights['시사점']}\n"
    
    # 완성된 텍스트를 파일로 저장!
    with open("final_report.md", "w", encoding="utf-8") as file:
        file.write(report_text)