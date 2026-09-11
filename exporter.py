import csv
import json
import logging

def export_to_csv(news_list, filename="exported_news.csv"):
    """
    뉴스 데이터를 CSV 파일로 내보내는 함수입니다.
    """
    if not news_list:
        logging.warning("내보낼 뉴스 데이터가 없습니다.")
        return False

    # 엑셀이나 CSV에서 한글이 깨지지 않도록 'utf-8-sig' 인코딩을 사용합니다.
    try:
        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            # 딕셔너리의 키값들을 표의 맨 위 제목(Header)으로 사용합니다.
            fieldnames = news_list[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader() # 제목 쓰기
            for news in news_list:
                writer.writerow(news) # 내용 쓰기
                
        logging.info(f"데이터 내보내기 성공: {filename} ({len(news_list)}건)")
        return True
    except Exception as e:
        logging.error(f"데이터 내보내기 실패: {e}")
        return False

    import json

def export_to_jsonl(news_list, filename="exported_news.jsonl"):
    """
    뉴스 데이터를 JSONL 파일로 내보내는 함수입니다.
    """
    if not news_list:
        logging.warning("내보낼 뉴스 데이터가 없습니다.")
        return False

    try:
        with open(filename, "w", encoding="utf-8") as file:
            for news in news_list:
                file.write(json.dumps(news, ensure_ascii=False) + "\n")

        logging.info(f"데이터 내보내기 성공: {filename} ({len(news_list)}건)")
        return True

    except Exception as e:
        logging.error(f"데이터 내보내기 실패: {e}")
        return False