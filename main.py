import argparse
import logging
import fetcher
import storage
import cleaner
import summarizer
import analyzer
import reporter
import exporter

# ⭐️ 파이썬 로깅 시스템 설정 (콘솔에 INFO 등급 이상의 로그를 예쁘게 출력해 줍니다)
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

parser = argparse.ArgumentParser(description="AI 뉴스 트렌드 및 종합 분석 리포트")
subparsers = parser.add_subparsers(dest="command")

# fetch 명령어
fetch_parser = subparsers.add_parser("fetch")
fetch_parser.add_argument("--source", default="google")
fetch_parser.add_argument("--limit", default=5) 

# clean 명령어
clean_parser = subparsers.add_parser("clean")

# summarize 명령어
summarize_parser = subparsers.add_parser("summarize")
summarize_parser.add_argument("--unsummarized", action="store_true")

# analyze 명령어
analyze_parser = subparsers.add_parser("analyze")
analyze_parser.add_argument("--category", default="IT")

# export 명령어
export_parser = subparsers.add_parser("export")
export_parser.add_argument("--status", default=None)
export_parser.add_argument("--format", choices=["csv", "jsonl"], default="csv")

# report 명령어
report_parser = subparsers.add_parser("report")

args = parser.parse_args()

if args.command == "fetch":
    logging.info(f"뉴스 수집 시작: source={args.source}, limit={args.limit}")
    collected_news = fetcher.fetch_google_news(args.limit)
    
    if collected_news:
        storage.save_raw_data(collected_news)
        logging.info(f"수집 완료: {len(collected_news)}건 성공")
        logging.info("raw 저장소(raw_news.jsonl)에 저장 완료!")
    else:
        logging.warning("수집된 뉴스가 없거나 네트워크 오류가 발생했습니다.")

elif args.command == "clean":
    logging.info("데이터 정제(Clean) 시작...")
    raw_data = storage.load_raw_data()
    cleaned_data = cleaner.clean_data(raw_data)
    storage.save_clean_data(cleaned_data)
    logging.info(f"정제 완료: {len(cleaned_data)}건 저장 (clean_news.jsonl)")

elif args.command == "summarize":
    logging.info("AI 뉴스 요약 시작...")
    clean_data = storage.load_clean_data()
    updated_data, count = summarizer.process_summaries(clean_data, option="unsummarized")
    storage.save_clean_data(updated_data)
    logging.info(f"요약 완료: {count}건 처리 완료!")

elif args.command == "analyze":
    logging.info(f"종합 인사이트 분석 시작 (카테고리: {args.category})...")
    clean_data = storage.load_clean_data()
    summarized_data = [news for news in clean_data if news.get("상태") == "summarized"]
    
    if not summarized_data:
        logging.warning("분석할 요약 뉴스가 없습니다. summarize를 먼저 실행해주세요.")
    else:
        insights = analyzer.generate_insights(summarized_data)
        storage.save_insights(insights)
        logging.info("분석 결과 저장 완료 (insight_result.json)")


elif args.command == "report":
    logging.info("최종 리포트 및 시각화 그래프 생성 중...")
    clean_data = storage.load_clean_data()
    insights = storage.load_insights()
    
    if not insights:
        logging.error("분석 결과가 없습니다. analyze를 먼저 실행해주세요.")
    else:
        reporter.generate_report(clean_data, insights)
        logging.info("리포트 및 그래프 생성 완료!")

elif args.command == "export":
    logging.info(f"데이터 내보내기 시작 (필터 상태: {args.status})...")

    clean_data = storage.load_clean_data()

    if args.status:
        target_data = [
            news for news in clean_data
            if news.get("상태") == args.status
        ]
    else:
        target_data = clean_data

    if args.format == "csv":
        exporter.export_to_csv(
        target_data,
        filename="exported_news.csv"
    )

    elif args.format == "jsonl": 
        exporter.export_to_jsonl(
        target_data,
        filename="exported_news.jsonl"
    )

else:
    logging.error("정확한 명령어를 입력해주세요. (fetch, clean, summarize, analyze, report)")