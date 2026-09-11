# 📰 AI 뉴스 트렌드 및 종합 분석 리포트 (News Manager)

## 1. 미션 소개

뉴스 데이터를 자동으로 수집하고 정제한 뒤, AI 기반 요약 및 트렌드 분석을 거쳐 시각화와 최종 리포트까지 생성하는 **CLI 기반 데이터 파이프라인 프로그램**이다.

단순히 뉴스 데이터를 가져오는 데 그치지 않고,

**뉴스 수집 → 원본 저장 → 데이터 정제 → 뉴스 요약 → 종합 인사이트 분석 → 시각화 → 리포트 생성 → 데이터 내보내기**

과정을 하나의 프로그램 안에서 연결하는 것을 목표로 제작했다.

프로그램은 Python의 `argparse`를 이용한 서브커맨드 방식으로 동작하며 `fetch`, `clean`, `summarize`, `analyze`, `report`, `export` 명령어를 각각 독립적으로 실행할 수 있도록 구성했다. 현재 GitHub의 `main.py`에도 6개의 필수 서브커맨드가 모두 등록되어 있다. ([GitHub][2])

또한 프로그램을 하나의 파일에 작성하지 않고 기능별 모듈로 분리하여 데이터 파이프라인의 각 단계가 서로 독립적으로 동작하도록 구성했다.

주요 모듈은 다음과 같다.

* `fetcher.py` : Google News RSS 뉴스 수집
* `storage.py` : JSONL 기반 데이터 저장 및 불러오기
* `cleaner.py` : 중복 제거 및 데이터 정제
* `summarizer.py` : 뉴스 요약 처리
* `analyzer.py` : 뉴스 트렌드 및 인사이트 생성
* `reporter.py` : 통계 계산, 그래프 및 리포트 생성
* `exporter.py` : CSV / JSONL 형식으로 데이터 내보내기
* `main.py` : 전체 CLI 명령어 제어

Git과 GitHub를 이용해 로컬 프로젝트를 원격 저장소와 연결하고, 기능 수정 이후 `commit`과 `push`를 수행하는 과정까지 직접 진행했다.

* **GitHub 저장소:** [https://github.com/riakwjddd06/news-manager](https://github.com/riakwjddd06/news-manager)
* **AI 활용 대화 로그:** [https://share.gemini.google/iKwwlmLQZdgO](https://share.gemini.google/iKwwlmLQZdgO)

---

## 2. 프로그램 실행 방법 및 기능별 시나리오

프로그램은 VSCode 터미널에서 실행하며, 일반적인 메뉴 선택 방식이 아니라 **CLI 서브커맨드 방식**으로 기능을 선택한다.

기본 명령어 형식은 다음과 같다.

```bash
python3 main.py [명령어] [옵션]
```

전체 도움말은 다음 명령어로 확인할 수 있다.

```bash
python3 main.py -h
```

현재 프로그램에는 다음 6개의 명령어가 등록되어 있다. ([GitHub][2])

```text
fetch
clean
summarize
analyze
report
export
```

### 📡 1. 뉴스 수집 — `fetch`

Google News의 Technology RSS를 이용해 뉴스를 수집한다.

```bash
python3 main.py fetch --source google --limit 5
```

옵션:

```text
--source : 뉴스 소스 지정
--limit  : 수집할 뉴스 개수 지정
```

현재 `fetcher.py`에서는 Google News의 한국어 Technology RSS 주소를 사용하며 `requests.get()`에 `timeout=5`를 지정해 네트워크 응답 시간이 지나치게 길어지는 상황을 방지하고 있다. HTTP 오류는 `raise_for_status()`와 예외 처리를 통해 로그로 기록하도록 구성했다. ([GitHub][3])

수집 데이터에는 다음 정보가 저장된다.

```json
{
    "제목": "뉴스 제목",
    "링크": "뉴스 URL",
    "수집시각": "2026-09-11 12:17:37",
    "소스정보": "google_rss",
    "수집방법": "rss",
    "카테고리": "IT"
}
```

수집된 데이터는 `raw_news.jsonl`에 저장된다.

---

### 🧼 2. 데이터 정제 — `clean`

```bash
python3 main.py clean
```

`raw_news.jsonl`을 불러온 뒤 정제 작업을 진행하고 결과를 `clean_news.jsonl`에 저장한다.

현재 정제 단계에서는 기사 링크를 기준으로 중복 여부를 검사하며 이미 등장한 링크는 `skip` 방식으로 제외한다. 또한 제목 앞뒤의 불필요한 공백을 제거하고 각 데이터에 `cleaned` 상태값을 부여한다. ([GitHub][4])

처리 흐름은 다음과 같다.

```text
raw_news.jsonl
        ↓
중복 링크 확인
        ↓
중복 기사 skip
        ↓
제목 공백 제거
        ↓
상태 = cleaned
        ↓
clean_news.jsonl
```

---

### 🤖 3. 뉴스 요약 — `summarize`

```bash
python3 main.py summarize --unsummarized
```

현재 `--unsummarized` 옵션을 이용해 아직 요약되지 않은 뉴스만 처리하도록 구성했다.

이미 `"요약"` 값이 존재하는 데이터는 다시 처리하지 않고 건너뛰며, 요약된 뉴스에는 다음 값이 추가된다.

```json
{
    "상태": "summarized",
    "요약": "[AI 요약] ..."
}
```

현재 저장소의 `summarizer.py`는 외부 AI API를 실제 호출하는 단계 이전의 **테스트용 요약 로직**으로 구성되어 있으며 뉴스 제목을 기반으로 요약 형식의 문자열을 생성한다. 코드 안에도 실제 API 연동 시 해당 부분에서 외부 AI API를 호출하도록 명시되어 있다. ([GitHub][5])

---

### 📊 4. 종합 인사이트 분석 — `analyze`

```bash
python3 main.py analyze --category IT
```

요약 상태가 `summarized`인 뉴스 데이터를 대상으로 종합 분석을 진행한다.

분석 결과는 다음 3가지 항목으로 구성했다.

* 주요 트렌드
* 핵심 키워드
* 시사점

결과는 별도의 `insight_result.json` 파일에 저장한다.

현재 저장소의 `analyzer.py` 역시 외부 AI API와 연결된 최종 형태가 아니라, 프로그램 전체 파이프라인을 검증하기 위해 미리 구성한 테스트용 인사이트 데이터를 반환하는 구조이다. 분석 결과에는 AI 기술의 확산, 글로벌 빅테크 경쟁, 자율주행 및 로봇 기술 확대 등의 트렌드와 핵심 키워드가 포함되어 있다. ([GitHub][6])

---

### 📈 5. 시각화 및 최종 리포트 — `report`

```bash
python3 main.py report
```

정제된 뉴스 데이터와 `insight_result.json`을 이용하여 그래프와 최종 마크다운 리포트를 생성한다.

생성 파일:

```text
news_chart.png
news_daily_trend.png
final_report.md
```

#### 카테고리별 뉴스 수

뉴스의 `"카테고리"` 값을 집계하여 막대그래프로 표시한다.

현재 수집 데이터는 Google News Technology RSS를 사용하므로 기본 카테고리는 `IT`이며, 향후 다른 카테고리를 추가할 경우 자동으로 여러 막대가 생성될 수 있도록 구현했다. ([GitHub][7])

#### 일자별 뉴스 수집 추이

뉴스의 `"수집시각"`에서 날짜 부분만 분리한 뒤 날짜별 기사 수를 계산하여 선 그래프로 표시한다. ([GitHub][7])

현재 테스트 데이터가 한 날짜에 수집된 5건이므로 그래프에는 하나의 날짜와 하나의 데이터 점이 표시되며, 여러 날짜의 데이터가 누적될 경우 선 그래프로 수집량 변화를 확인할 수 있다.

---

### 📦 6. 데이터 내보내기 — `export`

CSV와 JSONL 두 가지 형식을 지원한다.

#### CSV

```bash
python3 main.py export --format csv --status summarized
```

생성 파일:

```text
exported_news.csv
```

CSV 파일은 한글 깨짐을 줄이기 위해 `utf-8-sig` 인코딩을 사용한다. ([GitHub][8])

#### JSONL

```bash
python3 main.py export --format jsonl --status summarized
```

생성 파일:

```text
exported_news.jsonl
```

`--status summarized` 옵션을 이용하면 요약이 완료된 뉴스만 필터링하여 내보낼 수 있다. 이 필터링은 `main.py`에서 뉴스의 `"상태"` 값과 전달된 옵션값을 비교하는 방식으로 구현했다. ([GitHub][2])

---

## 3. 미션 수행 과정 및 트러블슈팅 내역

본 프로젝트는 AI의 도움을 받아 단계별로 구현 및 오류를 해결하면서 진행하였다.

### STEP 1. 뉴스 데이터 수집 구조 구현

먼저 뉴스 데이터를 수집할 소스를 선정했다.

중앙일보, 한겨레, 연합뉴스 등 국내 종합 뉴스 웹사이트의 직접 크롤링 방식도 검토했지만 사이트마다 HTML 구조와 접근 정책이 다르고, 동적 페이지 및 크롤링 제한 때문에 프로젝트 규모에 비해 구현 난도가 높아질 가능성이 있었다.

이에 따라 구조가 비교적 안정적이고 접근이 쉬운 **Google News RSS**를 수집 소스로 선택했다.

`requests`를 이용해 RSS 데이터를 요청하고, `BeautifulSoup(..., "xml")`을 이용하여 `<item>` 태그에서 제목과 링크를 추출하도록 구현했다. ([GitHub][3])

---

### STEP 2. 네트워크 타임아웃 및 오류 처리 추가

초기에는 단순히:

```python
requests.get(url)
```

형태로 요청했지만 네트워크가 끊기거나 서버 응답이 지연될 경우 프로그램 전체가 중단될 가능성이 있었다.

이를 보완하기 위해 다음과 같이 수정했다.

```python
response = requests.get(url, timeout=5)
response.raise_for_status()
```

그리고 다음 오류를 각각 처리했다.

```python
except requests.exceptions.Timeout:
    logging.error("서버 응답 시간이 초과되었습니다. (타임아웃)")

except requests.exceptions.RequestException as e:
    logging.error(f"네트워크 오류 발생: {e}")
```

현재 해당 처리 로직은 `fetcher.py`에 반영되어 있다. ([GitHub][3])

---

### STEP 3. Raw / Clean 데이터 분리

수집 데이터와 정제 데이터를 하나의 파일에서 관리하지 않고 역할별로 분리했다.

```text
raw_news.jsonl
→ 수집 직후의 원본 데이터

clean_news.jsonl
→ 중복 제거 및 정제가 끝난 데이터
```

`storage.py`에서는 JSONL 파일을 읽고 쓰는 함수를 별도로 구현하여 프로그램을 종료해도 데이터가 유지되도록 했다. 즉 리스트나 딕셔너리만 사용하는 메모리 기반 방식이 아니라 파일 기반 영구 저장 구조를 적용했다. ([GitHub][9])

---

### STEP 4. Logging 방식으로 출력 구조 변경

초기 코드에서는 다음과 같이 `print()`를 이용하고 있었다.

```python
print("[INFO] 뉴스 수집 시작...")
```

하지만 미션 요구사항에서 Python의 기본 `logging` 모듈을 이용해 `INFO`, `WARNING`, `ERROR` 레벨을 구분하도록 요구하고 있어 전체 CLI 출력 구조를 수정했다.

`main.py`에서 다음과 같이 로그 형식을 지정했다.

```python
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)
```

이후 실행 상황은 `logging.info()`, 문제가 발생할 수 있는 상황은 `logging.warning()`, 실패 상황은 `logging.error()`로 구분하였다. ([GitHub][2])

---

### STEP 5. `export` 명령어 구현 및 오류 해결

처음 `export` 기능을 실행했을 때:

```text
main.py: error: argument command: invalid choice: 'export'
```

오류가 발생했다.

이는 `argparse`의 서브커맨드 목록에 `export`가 등록되어 있지 않았기 때문이었다.

이에 다음 코드를 추가했다.

```python
export_parser = subparsers.add_parser("export")
export_parser.add_argument("--status", default=None)
export_parser.add_argument(
    "--format",
    choices=["csv", "jsonl"],
    default="csv"
)
```

이후 다시 실행했을 때:

```text
AttributeError:
module 'exporter' has no attribute 'export_to_csv'
```

오류가 발생했다.

`exporter.py`의 저장 상태 및 함수 정의 여부를 확인한 뒤 `export_to_csv()`를 정상적으로 구현하여 CSV 내보내기에 성공했다.

이후 JSONL 내보내기를 추가하는 과정에서는:

```text
name 'json' is not defined
```

오류가 발생했다.

원인은 `json.dumps()`를 사용하면서 `import json`이 누락된 것이었고, `exporter.py` 상단에:

```python
import json
```

을 추가하여 해결했다.

최종적으로:

```text
exported_news.csv
exported_news.jsonl
```

두 포맷 모두 정상적으로 생성되었다.

현재 `exporter.py`는 CSV와 JSONL 내보내기 기능을 모두 포함한다. ([GitHub][8])

---

### STEP 6. 시각화 2종 구현

초기 리포트에는 전체 뉴스 건수를 보여주는 막대그래프 한 개만 존재했다.

미션에서 요구하는:

```text
카테고리별 뉴스 수
일자별 수집 추이
```

두 가지 그래프를 충족하기 위해 `reporter.py`를 수정했다.

첫 번째 그래프는 각 뉴스의 `"카테고리"` 값을 집계하고, 두 번째 그래프는 `"수집시각"`을 날짜 기준으로 묶어 일별 뉴스 수를 계산하도록 구현했다. ([GitHub][7])

#### 트러블슈팅 — matplotlib 오류

막대그래프를 생성하는 과정에서 다음 오류가 발생했다.

```text
TypeError:
only 0-dimensional arrays can be converted to Python scalars
```

오류가 기존 `plt.bar()` 처리 과정에서 발생한 것을 확인한 후 막대 테두리 두께를 명확하게 지정했다.

```python
plt.bar(
    categories,
    counts,
    color="skyblue",
    linewidth=0
)
```

수정 후 `report` 명령어가 정상적으로 완료되었으며:

```text
news_chart.png
news_daily_trend.png
```

두 개의 그래프 파일을 생성하는 데 성공했다.

---

### STEP 7. 카테고리 데이터 추가

기존 `clean_news.jsonl`을 확인했을 때 `"카테고리"` 필드가 존재하지 않는 것을 발견했다.

이에 새로 수집되는 뉴스 데이터에 다음 값을 추가했다.

```python
"카테고리": "IT"
```

또한 기존 데이터처럼 카테고리 값이 없는 경우에도 리포트 생성이 실패하지 않도록 다음과 같이 기본값을 지정했다.

```python
category = news.get("카테고리", "IT")
```

현재 `fetcher.py`에는 수집 데이터의 카테고리가 `IT`로 저장되도록 반영되어 있다. ([GitHub][3])

---

### STEP 8. 리포트 품질 지표 보강

초기 `final_report.md`에는 뉴스 개수와 AI 인사이트만 존재했다.

미션 요구사항의:

```text
품질 지표 2개 이상
TOP N 집계 1개 이상
AI 인사이트
```

조건을 충족하도록 `reporter.py`를 보완했다.

#### 품질 지표 1 — 요약 완료율

```python
summary_rate =
    summarized_count / news_count * 100
```

전체 뉴스 중 `"상태": "summarized"`인 기사의 비율을 계산했다.

#### 품질 지표 2 — 필수 필드 충족률

필수 데이터 항목을 다음과 같이 설정했다.

```python
required_fields = [
    "제목",
    "링크",
    "수집시각"
]
```

모든 필수 필드가 존재하는 데이터 수를 계산한 뒤 전체 데이터 수와 비교해 비율을 구했다.

현재 최종 리포트에서는 테스트 데이터 5건 모두가 요약 완료 및 필수 필드 충족 상태로 집계되어 각각 `100.00%`로 표시된다. ([GitHub][10])

---

### STEP 9. TOP N 집계 추가

카테고리별 뉴스 수를 많은 순서대로 정렬한 뒤 상위 3개만 선택하도록 구현했다.

```python
top_categories = sorted(
    category_counts.items(),
    key=lambda x: x[1],
    reverse=True
)[:3]
```

현재 데이터에는 IT 카테고리만 존재하므로:

```text
1. IT - 5건
```

으로 출력되며, 향후 여러 뉴스 카테고리를 수집하면 최대 3개까지 자동으로 정렬되어 표시된다.

GitHub에 저장된 현재 최종 리포트에서도 `카테고리 TOP 3` 섹션과 IT 5건 집계가 확인된다. ([GitHub][10])

---

### STEP 10. Git 저장소 초기화 및 GitHub 연동

프로젝트 개발 도중 GitHub 연결 상태를 확인하기 위해:

```bash
git remote -v
git status
```

를 실행했으나 처음에는:

```text
fatal: not a git repository
```

오류가 발생했다.

현재 프로젝트 폴더가 Git 저장소로 초기화되어 있지 않은 상태라는 것을 확인하고:

```bash
git init
```

을 실행했다.

이후 GitHub에 생성한 `news-manager` 저장소를 다음 명령어로 연결했다.

```bash
git remote add origin https://github.com/riakwjddd06/news-manager.git
```

그리고:

```bash
git remote -v
```

로 `fetch`, `push` 주소가 모두 등록된 것을 확인했다.

---

### STEP 11. `.gitignore` 설정

API 키나 실행 중 자동 생성되는 파일이 GitHub에 올라가는 것을 방지하기 위해 `.gitignore`를 구성했다.

현재 저장소의 `.gitignore`에는 다음 항목이 존재한다. ([GitHub][11])

```text
__pycache__/
*.pyc
.env
config.json
exported_news.csv
exported_news.jsonl
```

특히 `config.json`은 API 키와 설정값이 포함될 가능성이 있어 Git 추적 대상에서 제외했다.

또한 `exported_news.csv`, `exported_news.jsonl`은 프로그램을 실행할 때 생성되는 결과 파일이므로 GitHub에서 제외했다.

반면 과제 결과를 증명할 수 있는:

```text
news_chart.png
news_daily_trend.png
final_report.md
```

는 저장소에 포함했다.

---

### STEP 12. Git 커밋 및 Push

수정 파일을:

```bash
git add .
```

로 staging한 뒤:

```bash
git commit -m "feat: complete export visualization and report"
```

를 실행했다.

커밋 결과:

```text
8 files changed
208 insertions(+)
43 deletions(-)
```

이 출력되었으며 두 번째 그래프인 `news_daily_trend.png`도 새 파일로 포함되었다.

마지막으로:

```bash
git push
```

를 실행하여 로컬 `main` 브랜치의 변경사항을 GitHub 원격 저장소의 `main` 브랜치에 정상 반영했다.

현재 GitHub 저장소에는 2개의 커밋과 프로젝트 모듈 및 결과 파일이 공개되어 있다. ([GitHub][1])

---

## 4. 파이썬 코드 상세 설명

### `main.py` — 전체 프로그램 제어

`main.py`는 데이터 파이프라인 전체를 제어하는 진입점이다.

`argparse`를 이용해 다음 서브커맨드를 정의한다.

```python
fetch
clean
summarize
analyze
export
report
```

각 명령어가 입력되면 해당 기능을 담당하는 모듈의 함수를 호출한다.

예를 들어 `fetch`의 흐름은:

```python
collected_news = fetcher.fetch_google_news(args.limit)
storage.save_raw_data(collected_news)
```

형태이고, `clean`은:

```python
raw_data = storage.load_raw_data()
cleaned_data = cleaner.clean_data(raw_data)
storage.save_clean_data(cleaned_data)
```

형태로 작동한다.

즉 `main.py`는 직접 모든 작업을 수행하기보다는 각 전문 모듈을 연결하는 **파이프라인 제어기 역할**을 담당한다. ([GitHub][2])

---

### `fetcher.py` — 뉴스 데이터 수집

주요 라이브러리:

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
```

Google News RSS를 요청한 뒤 XML을 파싱한다.

```python
response = requests.get(url, timeout=5)
response.raise_for_status()

soup = BeautifulSoup(response.text, "xml")
items = soup.find_all("item")
```

각 `<item>`에서 뉴스 제목과 링크를 읽고 수집시각, 소스, 수집방법, 카테고리를 함께 저장한다. ([GitHub][3])

---

### `storage.py` — 데이터 영구 저장

데이터는 JSONL 형식을 이용한다.

```text
raw_news.jsonl
clean_news.jsonl
```

한 줄에 하나의 JSON 객체를 저장하기 때문에 여러 뉴스 데이터를 순차적으로 추가하거나 읽기 쉽다.

원본 뉴스는 append 방식으로 저장하고:

```python
with open(
    "raw_news.jsonl",
    "a",
    encoding="utf-8"
)
```

정제 데이터는 새 상태를 반영하기 위해 write 방식으로 저장한다.

```python
with open(
    "clean_news.jsonl",
    "w",
    encoding="utf-8"
)
```

이를 통해 프로그램을 종료해도 데이터가 유지되는 **영구 저장 구조**를 구현했다. ([GitHub][9])

---

### `cleaner.py` — 중복 제거 및 데이터 정제

중복 확인에는 Python의 `set()` 자료구조를 이용한다.

```python
seen_links = set()
```

이미 등장한 링크라면:

```python
if news["링크"] in seen_links:
    continue
```

로 넘어간다.

처음 보는 링크만:

```python
seen_links.add(news["링크"])
```

로 저장한다.

이 방식으로 같은 링크가 여러 번 수집되더라도 하나만 남도록 **skip 중복 정책**을 적용했다. ([GitHub][4])

---

### `summarizer.py` — 뉴스 요약 처리

뉴스 목록을 순회하며 이미 요약된 데이터인지 확인한다.

```python
already_done = (
    "요약" in news and news["요약"] != ""
)
```

이미 처리된 뉴스는 `--unsummarized` 조건에서 건너뛴다.

```python
if option == "unsummarized" and already_done:
    continue
```

새롭게 요약된 뉴스에는:

```python
news["상태"] = "summarized"
```

를 지정한다.

현재 구현은 테스트용 요약문을 생성하는 단계이며 실제 AI API 호출부는 향후 확장할 수 있도록 분리되어 있다. ([GitHub][5])

---

### `analyzer.py` — 뉴스 트렌드 분석

요약된 뉴스 목록을 전달받아 분석 결과를 다음 구조로 반환한다.

```python
{
    "주요_트렌드": [...],
    "핵심_키워드": [...],
    "시사점": "..."
}
```

현재 테스트 로직에서는 주요 트렌드 3개, 핵심 키워드 5개, 시사점 1개를 생성한다. ([GitHub][6])

---

### `reporter.py` — 그래프 및 최종 리포트 생성

`matplotlib`을 이용해 두 종류의 PNG 그래프를 생성한다.

#### 카테고리별 뉴스 수

```python
category_counts = {}

for news in news_list:
    category = news.get("카테고리", "IT")
    category_counts[category] = (
        category_counts.get(category, 0) + 1
    )
```

#### 일자별 수집 추이

```python
daily_counts = {}

for news in news_list:
    collected_at = news.get("수집시각", "")

    if collected_at:
        date = collected_at.split(" ")[0]
        daily_counts[date] = (
            daily_counts.get(date, 0) + 1
        )
```

결과를 각각:

```text
news_chart.png
news_daily_trend.png
```

로 저장한다. ([GitHub][7])

마지막으로 품질 지표와 TOP N, AI 인사이트를 하나의 문자열로 조합하여:

```text
final_report.md
```

를 생성한다.

---

### `exporter.py` — 데이터 내보내기

CSV 출력은 `csv.DictWriter`를 이용한다.

```python
writer = csv.DictWriter(
    file,
    fieldnames=fieldnames
)

writer.writeheader()

for news in news_list:
    writer.writerow(news)
```

JSONL은 각각의 딕셔너리를 `json.dumps()`로 변환해 한 줄씩 작성한다.

내보낼 데이터가 없거나 파일 작성 도중 예외가 발생하면 `logging.warning()` 또는 `logging.error()`를 통해 로그를 출력한다. ([GitHub][8])

---

## 5. 최종 결과 및 산출물

### 1. GitHub 저장소

프로젝트 전체 코드 및 결과 파일:

**[https://github.com/riakwjddd06/news-manager](https://github.com/riakwjddd06/news-manager)**

현재 저장소에는 다음 주요 파일이 포함되어 있다. ([GitHub][1])

```text
.gitignore
analyzer.py
clean_news.jsonl
cleaner.py
exporter.py
fetcher.py
final_report.md
insight_result.json
main.py
news_chart.png
news_daily_trend.png
raw_news.jsonl
reporter.py
storage.py
summarizer.py
```

---

### 2. 뉴스 수집 결과

```text
raw_news.jsonl
```

Google News RSS에서 가져온 원본 뉴스 데이터가 저장된다.

---

### 3. 정제 결과

```text
clean_news.jsonl
```

중복 제거 및 텍스트 정제가 완료된 뉴스 데이터가 저장된다.

---

### 4. AI 인사이트 결과

```text
insight_result.json
```

주요 트렌드, 핵심 키워드, 시사점을 별도 JSON 파일로 저장한다.

---

### 5. 시각화 결과

```text
news_chart.png
news_daily_trend.png
```

각각:

* 카테고리별 뉴스 수
* 일자별 뉴스 수집 추이

를 시각화한다.

현재 GitHub 저장소에도 두 PNG 결과물이 모두 포함되어 있다. ([GitHub][1])

---

### 6. 최종 종합 리포트

```text
final_report.md
```

현재 생성된 리포트에는:

* 총 수집 뉴스 수
* 요약 완료 건수 및 비율
* 필수 필드 충족 데이터
* 분석 상태
* 카테고리 TOP 3
* 주요 트렌드
* 핵심 키워드
* 시사점

이 포함되어 있다. 현재 데이터 기준으로 총 5건, 요약 완료율 100%, IT 카테고리 5건이 기록되어 있다. ([GitHub][10])

---

### 7. 데이터 내보내기 결과

```text
exported_news.csv
exported_news.jsonl
```

두 파일은 정상 생성되는 것을 확인했으며 실행 결과물이므로 `.gitignore`에 등록해 GitHub에는 업로드하지 않도록 처리했다. ([GitHub][11])

---

## 6. 트러블슈팅 요약

| 오류 및 문제                                   | 원인                          | 해결 방법                           |
| ----------------------------------------- | --------------------------- | ------------------------------- |
| `fatal: not a git repository`             | 프로젝트가 Git 저장소로 초기화되지 않음     | `git init` 실행                   |
| GitHub 원격 저장소 미연결                         | `origin` 주소 미등록             | `git remote add origin ...` 실행  |
| `invalid choice: 'export'`                | argparse에 `export` 서브커맨드 누락 | `export_parser` 추가              |
| `exporter has no attribute export_to_csv` | 함수 저장 또는 정의 문제              | `export_to_csv()` 구현 및 저장       |
| `name 'json' is not defined`              | `import json` 누락            | `exporter.py`에 `import json` 추가 |
| Matplotlib `TypeError`                    | 막대그래프 내부 linewidth 처리 문제    | `linewidth=0` 명시                |
| 카테고리 데이터 없음                               | 기존 수집 데이터에 필드 미포함           | `"카테고리": "IT"` 추가 및 기본값 처리      |
| 그래프 1종만 존재                                | 일자별 추이 그래프 미구현              | `news_daily_trend.png` 추가       |
| 리포트 품질 지표 부족                              | 통계 계산 미구현                   | 요약 완료율, 필수 필드 충족률 추가            |
| TOP N 집계 누락                               | 카테고리 순위 미계산                 | 카테고리 TOP 3 구현                   |
| 자동 생성 export 파일 Git 추적                    | `.gitignore` 미등록            | CSV / JSONL 결과 파일 제외            |

---

## 7. 구현을 통해 확인한 데이터 파이프라인 구조

이번 프로젝트의 전체 데이터 흐름은 다음과 같다.

```text
Google News RSS
       │
       ▼
    fetch
       │
       ▼
raw_news.jsonl
       │
       ▼
    clean
       │
       ▼
clean_news.jsonl
       │
       ▼
  summarize
       │
       ▼
summarized 상태 뉴스
       │
       ▼
    analyze
       │
       ▼
insight_result.json
       │
       ├───────────────┐
       ▼               ▼
    report           export
       │               │
       ▼               ├── CSV
news_chart.png          │
news_daily_trend.png    └── JSONL
final_report.md
```

각 기능을 독립된 Python 모듈로 나누면서 한 단계의 출력 결과가 다음 단계의 입력 데이터가 되는 **데이터 파이프라인 구조**를 실제 코드로 구현할 수 있었다.

---

## 8. 현재 구현 상태 및 향후 보완 사항

현재 프로젝트에서는 CLI 구조, RSS 뉴스 수집, JSONL 영구 저장, 중복 제거, 로깅, 네트워크 오류 처리, CSV/JSONL 내보내기, 시각화 2종, 품질 지표, TOP N 집계 및 최종 리포트 생성까지 구현했다.

다만 저장소의 현재 코드를 기준으로 보면 **AI 요약과 인사이트 분석은 실제 외부 AI API를 호출하는 형태가 아니라 테스트용 로직으로 구현되어 있다.** `summarizer.py` 역시 실제 API 연동 위치를 주석으로 표시하고 있다. ([GitHub][5])

따라서 향후 완성도를 높이기 위해 다음 기능을 추가할 수 있다.

* 실제 AI API와 `summarizer.py` 연결
* 실제 뉴스 데이터를 기반으로 `analyzer.py`에서 트렌드 생성
* `summarize --all`, `--id` 옵션 추가
* `analyze --date-from`, `--date-to` 기간 필터 추가
* 경제·사회·정치 등 여러 Google News RSS 카테고리 지원
* 중복 제거율 등 추가 품질 지표 계산
* `list`, `show` 뉴스 조회 CLI 구현
* 감성 분석 기능 추가
* README에 실행 방법 및 정기 실행 방법 문서화

특히 현재 `main.py`에서는 `fetch`, `clean`, `summarize`, `analyze`, `export`, `report`의 필수 명령어가 모두 구현되어 있고, `export`는 CSV와 JSONL 두 가지 포맷을 지원한다. ([GitHub][2])

---

## 9. 최종 소감

이번 프로젝트를 통해 단순히 Python 코드를 한 파일에서 실행하는 것과 여러 기능을 **하나의 데이터 파이프라인으로 연결하는 것의 차이**를 경험할 수 있었다.

특히 기능을 구현하는 과정에서 단순히 정상 동작하는 코드를 작성하는 것뿐만 아니라, 네트워크 오류를 대비한 예외 처리, `logging`을 통한 실행 상태 관리, Raw/Clean 데이터 분리, Git에서 제외해야 하는 파일 관리, 기능별 모듈 분리와 같이 실제 프로그램 구조에서 필요한 요소들을 함께 적용했다.

또한 `AttributeError`, `NameError`, Matplotlib 관련 `TypeError`, Git 저장소 초기화 문제 등 여러 오류를 직접 확인하고 원인을 하나씩 추적해 수정하면서 **오류 메시지를 읽고 문제 발생 위치를 찾는 디버깅 과정**을 경험했다.

최종적으로 뉴스 수집부터 저장, 정제, 요약, 분석, 시각화, 리포트, 데이터 내보내기까지 이어지는 전체 흐름을 구현하면서 데이터 파이프라인의 각 단계가 어떤 역할을 하는지 보다 구체적으로 이해할 수 있었다.

[1]: https://github.com/riakwjddd06/news-manager "GitHub - riakwjddd06/news-manager · GitHub"
[2]: https://github.com/riakwjddd06/news-manager/blob/main/main.py "news-manager/main.py at main · riakwjddd06/news-manager · GitHub"
[3]: https://github.com/riakwjddd06/news-manager/blob/main/fetcher.py "news-manager/fetcher.py at main · riakwjddd06/news-manager · GitHub"
[4]: https://github.com/riakwjddd06/news-manager/blob/main/cleaner.py "news-manager/cleaner.py at main · riakwjddd06/news-manager · GitHub"
[5]: https://github.com/riakwjddd06/news-manager/blob/main/summarizer.py "news-manager/summarizer.py at main · riakwjddd06/news-manager · GitHub"
[6]: https://github.com/riakwjddd06/news-manager/blob/main/analyzer.py "news-manager/analyzer.py at main · riakwjddd06/news-manager · GitHub"
[7]: https://github.com/riakwjddd06/news-manager/blob/main/reporter.py "news-manager/reporter.py at main · riakwjddd06/news-manager · GitHub"
[8]: https://github.com/riakwjddd06/news-manager/blob/main/exporter.py "news-manager/exporter.py at main · riakwjddd06/news-manager · GitHub"
[9]: https://github.com/riakwjddd06/news-manager/blob/main/storage.py "news-manager/storage.py at main · riakwjddd06/news-manager · GitHub"
[10]: https://github.com/riakwjddd06/news-manager/blob/main/final_report.md "news-manager/final_report.md at main · riakwjddd06/news-manager · GitHub"
[11]: https://github.com/riakwjddd06/news-manager/blob/main/.gitignore "news-manager/.gitignore at main · riakwjddd06/news-manager · GitHub"
