import json
import os

def save_raw_data(news_list):
    with open("raw_news.jsonl", "a", encoding="utf-8") as file:
        for news in news_list:
            file.write(json.dumps(news, ensure_ascii=False) + "\n")

def load_raw_data():
    if not os.path.exists("raw_news.jsonl"):
        return []
    news_list = []
    with open("raw_news.jsonl", "r", encoding="utf-8") as file:
        for line in file:
            news_list.append(json.loads(line))
    return news_list

# ⭐️ Clean 창고에서 읽어오기 기능 추가
def load_clean_data():
    if not os.path.exists("clean_news.jsonl"):
        return []
    news_list = []
    with open("clean_news.jsonl", "r", encoding="utf-8") as file:
        for line in file:
            news_list.append(json.loads(line))
    return news_list

def save_clean_data(news_list):
    with open("clean_news.jsonl", "w", encoding="utf-8") as file:
        for news in news_list:
            file.write(json.dumps(news, ensure_ascii=False) + "\n")

 # ⭐️ 분석 결과를 별도로 저장하는 기능 추가
def save_insights(insights_data):
    with open("insight_result.json", "w", encoding="utf-8") as file:
        json.dump(insights_data, file, ensure_ascii=False, indent=4)

 # ⭐️ 저장된 인사이트(분석) 결과를 불러오는 기능
def load_insights():
    if not os.path.exists("insight_result.json"):
        return None
    with open("insight_result.json", "r", encoding="utf-8") as file:
        return json.load(file)