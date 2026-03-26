# Python 웹 크롤링

## 목차
1. [개요](#개요)
2. [환경 설정](#환경-설정)
3. [정적 페이지 크롤링 (BeautifulSoup)](#정적-페이지-크롤링)
4. [동적 페이지 크롤링 (Selenium)](#동적-페이지-크롤링)
5. [실전 예제](#실전-예제)
6. [주의사항](#주의사항)

---

## 빠른 시작

### 1단계: 라이브러리 설치

```bash
# 정적 크롤링 (필수)
pip install requests beautifulsoup4 lxml pandas

# 동적 크롤링 (선택)
pip install selenium webdriver-manager
```

### 2단계: 연결 테스트

```bash
# 테스트 실행
python test_crawling.py
# 또는
test_crawling.bat
```

### 3단계: 예제 실행

```bash
# 정적 크롤링 예제
python crawling_example_static.py
# 또는
run_crawling_static.bat

# 동적 크롤링 예제
python crawling_example_dynamic.py
# 또는
run_crawling_dynamic.bat
```

---

## 파일 구조

```
c:\python_streamlit\
├── WEB_CRAWLING_GUIDE.md          # 완전 가이드 (이론)
├── crawling_example_static.py     # 정적 크롤링 예제
├── crawling_example_dynamic.py    # 동적 크롤링 예제
├── test_crawling.py               # 연결 테스트
├── test_crawling.bat              # 테스트 실행 (배치)
├── run_crawling_static.bat        # 정적 예제 실행 (배치)
└── run_crawling_dynamic.bat       # 동적 예제 실행 (배치)
```

---

## 정적 크롤링 예제

### 크롤링 대상 사이트

1. **Hacker News** (https://news.ycombinator.com/)
   - 실제 기술 뉴스 사이트
   - 헤드라인, 링크 수집

2. **Wikipedia** (https://en.wikipedia.org/)
   - 프로그래밍 언어 목록
   - 테이블 데이터 추출

3. **Books to Scrape** (http://books.toscrape.com/)
   - 크롤링 연습용 서점
   - 제품 정보, 가격, 평점

4. **GitHub Trending** (https://github.com/trending)
   - 인기 저장소 목록
   - 스타 수, 설명

5. **Quotes to Scrape** (http://quotes.toscrape.com/)
   - 명언 수집
   - 여러 페이지 크롤링

### 실행 방법

```bash
python crawling_example_static.py
```

### 생성되는 파일

- `hackernews_data.csv` - Hacker News 헤드라인
- `programming_languages.csv` - 프로그래밍 언어 목록
- `books_data.csv` - 책 정보
- `github_trending.csv` - GitHub 인기 저장소
- `quotes_data.csv` - 명언 모음

---

## 동적 크롤링 예제

### 크롤링 대상

1. **JavaScript 콘텐츠** (http://quotes.toscrape.com/js/)
   - JavaScript로 생성되는 명언
   - 동적 로딩 대기

2. **무한 스크롤** (http://quotes.toscrape.com/scroll)
   - 스크롤 이벤트 처리
   - 중복 제거

3. **버튼 클릭 페이지네이션**
   - Next 버튼 클릭
   - 여러 페이지 수집

4. **스크린샷 저장**
   - 전체 페이지 캡처
   - 특정 요소 캡처

### 실행 방법

```bash
python crawling_example_dynamic.py
```

️ **주의**: Chrome 브라우저가 자동으로 실행됩니다.

### 생성되는 파일

- `quotes_js_data.csv` - JavaScript 명언
- `quotes_scroll_data.csv` - 무한 스크롤 명언
- `quotes_pagination.csv` - 페이지네이션 명언
- `page_screenshot.png` - 페이지 스크린샷
- `quote_screenshot.png` - 요소 스크린샷

---

## 개요

### 크롤링이란?
웹사이트에서 데이터를 자동으로 수집하는 기술입니다.

### 정적 vs 동적 페이지

| 구분 | 정적 페이지 | 동적 페이지 |
|------|------------|------------|
| **특징** | HTML이 완성된 상태로 제공 | JavaScript로 콘텐츠 생성 |
| **예시** | 뉴스 기사, 블로그 | 인스타그램, 페이스북 |
| **도구** | BeautifulSoup + requests | Selenium + ChromeDriver |
| **속도** | 빠름 | 느림 |
| **난이도** | 쉬움 | 어려움 |

---

## 환경 설정

### 1단계: 필수 라이브러리 설치

```bash
# 정적 페이지 크롤링
pip install requests beautifulsoup4 lxml

# 동적 페이지 크롤링
pip install selenium

# 데이터 처리
pip install pandas
```

### 2단계: ChromeDriver 설치 (Selenium 사용 시)

#### 방법 1: 수동 설치
1. Chrome 버전 확인: `chrome://version/`
2. [ChromeDriver 다운로드](https://chromedriver.chromium.org/)
3. PATH에 추가 또는 프로젝트 폴더에 저장

#### 방법 2: 자동 설치 (권장)
```bash
pip install webdriver-manager
```

### 3단계: requirements.txt 생성

```txt
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
selenium==4.15.2
webdriver-manager==4.0.1
pandas==2.1.3
```

설치:
```bash
pip install -r requirements.txt
```

---

## 정적 페이지 크롤링

### 기본 구조

```python
import requests
from bs4 import BeautifulSoup

# 1. HTTP 요청
url = "https://example.com"
response = requests.get(url)

# 2. HTML 파싱
soup = BeautifulSoup(response.text, 'lxml')

# 3. 데이터 추출
title = soup.find('h1').text
print(title)
```

### 1단계: HTTP 요청 (requests)

```python
import requests

# 기본 GET 요청
response = requests.get('https://example.com')

# 헤더 추가 (봇 차단 방지)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get('https://example.com', headers=headers)

# 응답 확인
print(response.status_code)  # 200: 성공
print(response.encoding)     # 인코딩 확인
print(response.text)         # HTML 내용
```

#### 주요 메서드

```python
# GET 요청 (데이터 조회)
requests.get(url, params={'key': 'value'})

# POST 요청 (데이터 전송)
requests.post(url, data={'key': 'value'})

# 세션 유지 (로그인 등)
session = requests.Session()
session.get(url)
```

### 2단계: HTML 파싱 (BeautifulSoup)

```python
from bs4 import BeautifulSoup

html = """
<html>
  <head><title>샘플 페이지</title></head>
  <body>
    <h1 class="main-title">제목</h1>
    <div id="content">
      <p class="text">첫 번째 문단</p>
      <p class="text">두 번째 문단</p>
      <a href="/page1">링크1</a>
      <a href="/page2">링크2</a>
    </div>
  </body>
</html>
"""

soup = BeautifulSoup(html, 'lxml')
```

#### 데이터 찾기 메서드

```python
# 1. find() - 첫 번째 요소만
title = soup.find('h1')
print(title.text)  # 제목

# 2. find_all() - 모든 요소
paragraphs = soup.find_all('p')
for p in paragraphs:
    print(p.text)

# 3. CSS 선택자 (select)
# class로 찾기
texts = soup.select('.text')

# id로 찾기
content = soup.select('#content')

# 복합 선택자
links = soup.select('div#content a')
```

#### 속성 접근

```python
# 위의 HTML 예제 사용 (a 태그와 img 태그 포함)
html = """
<html>
  <body>
    <a href="/page1">링크1</a>
    <a href="/page2">링크2</a>
    <img src="/image1.jpg" alt="이미지1">
    <img src="/image2.jpg" alt="이미지2">
  </body>
</html>
"""
soup = BeautifulSoup(html, 'html.parser')

# href 속성 가져오기
link = soup.find('a')
print(link['href'])        # /page1
print(link.get('href'))    # /page1 (안전)

# 모든 링크 추출
links = soup.find_all('a')
for link in links:
    print(link.get('href'))  # /page1, /page2

# 이미지 src 추출
img = soup.find('img')
print(img.get('src'))  # /image1.jpg

# 속성이 없을 때 안전하게 처리
link_without_href = soup.find('a')  # href가 없는 경우
# link['href']  # KeyError 발생!
href = link.get('href', '#')  # 기본값 '#' 반환
```

**중요:** 속성이 없을 수 있으므로 `get()` 메서드 사용을 권장합니다.

### 3단계: 데이터 정제

```python
# 공백 제거
text = soup.find('p').text.strip()

# 여러 줄 처리
text = soup.find('div').get_text(separator='\n', strip=True)

# 숫자 추출
import re
price = "가격: 15,000원"
number = int(re.sub(r'[^0-9]', '', price))  # 15000
```

### 실습 예제 1: 실제 사이트 크롤링 (Books to Scrape)

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_books():
    """온라인 서점 책 정보 크롤링 (실제 실행 가능)"""
    
    url = "http://books.toscrape.com/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # 요청
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 에러 체크
    
    # 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 데이터 수집
    books = []
    
    # 책 목록 찾기
    articles = soup.select('article.product_pod')[:10]  # 상위 10개
    
    for article in articles:
        # 제목
        title = article.select_one('h3 a').get('title')
        
        # 가격
        price = article.select_one('.price_color').text
        
        # 재고
        stock = article.select_one('.availability').text.strip()
        
        # 평점
        rating_class = article.select_one('.star-rating').get('class')[1]
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = rating_map.get(rating_class, 0)
        
        books.append({
            'title': title,
            'price': price,
            'stock': stock,
            'rating': rating
        })
    
    # DataFrame 변환
    df = pd.DataFrame(books)
    return df

# 실행
if __name__ == '__main__':
    books_df = crawl_books()
    print(books_df)
    
    # CSV 저장
    books_df.to_csv('books_crawled.csv', index=False, encoding='utf-8-sig')
    print(" books_crawled.csv 저장 완료")
```

### 실습 예제 2: 여러 페이지 크롤링

```python
import requests
from bs4 import BeautifulSoup
import time

def crawl_quotes(pages=3):
    """명언 사이트 여러 페이지 크롤링 (실제 실행 가능)"""
    
    all_quotes = []
    
    for page in range(1, pages + 1):
        print(f"페이지 {page} 크롤링 중...")
        
        url = f"http://quotes.toscrape.com/page/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 명언 추출
        quotes = soup.select('.quote')
        
        for quote in quotes:
            text = quote.select_one('.text').text
            author = quote.select_one('.author').text
            tags = [tag.text for tag in quote.select('.tag')]
            
            all_quotes.append({
                'quote': text,
                'author': author,
                'tags': ', '.join(tags)
            })
        
        time.sleep(0.5)  # 서버 부담 방지
    
    return all_quotes

# 실행
quotes = crawl_quotes(pages=3)
print(f"총 {len(quotes)}개의 명언 수집")
```

---

## 동적 페이지 크롤링

### Selenium 기본 구조

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# 1. 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 2. 페이지 열기
driver.get('https://example.com')

# 3. 요소 찾기
element = driver.find_element(By.CSS_SELECTOR, '.class-name')

# 4. 데이터 추출
text = element.text

# 5. 종료
driver.quit()
```

### 1단계: 드라이버 설정

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 옵션 설정
options = Options()

# 헤드리스 모드 (브라우저 창 안 띄우기)
options.add_argument('--headless')

# 기타 유용한 옵션
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

# User-Agent 설정
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

# 드라이버 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```

### 2단계: 요소 찾기 (By)

```python
from selenium.webdriver.common.by import By

# CSS Selector (권장)
element = driver.find_element(By.CSS_SELECTOR, '.class-name')

# ID
element = driver.find_element(By.ID, 'element-id')

# Class Name
element = driver.find_element(By.CLASS_NAME, 'class-name')

# XPath
element = driver.find_element(By.XPATH, '//div[@class="class-name"]')

# Tag Name
elements = driver.find_elements(By.TAG_NAME, 'a')

# Link Text
element = driver.find_element(By.LINK_TEXT, '로그인')

# Partial Link Text
element = driver.find_element(By.PARTIAL_LINK_TEXT, '로그')
```

### 3단계: 대기 (Wait)

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# 명시적 대기 (Explicit Wait) - 권장
wait = WebDriverWait(driver, 10)  # 최대 10초 대기

# 요소가 나타날 때까지 대기
element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.dynamic-content'))
)

# 요소가 클릭 가능할 때까지 대기
button = wait.until(
    EC.element_to_be_clickable((By.ID, 'submit-button'))
)

# 암묵적 대기 (Implicit Wait)
driver.implicitly_wait(10)  # 모든 요소에 최대 10초 대기

# 강제 대기 (비권장)
time.sleep(3)  # 3초 대기
```

### 4단계: 인터랙션

```python
from selenium.webdriver.common.keys import Keys

# 클릭
button = driver.find_element(By.ID, 'submit-btn')
button.click()

# 텍스트 입력
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('검색어')
search_box.send_keys(Keys.ENTER)

# 스크롤
# 페이지 끝까지
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 특정 요소까지
element = driver.find_element(By.ID, 'footer')
driver.execute_script("arguments[0].scrollIntoView();", element)

# JavaScript 실행
driver.execute_script("alert('Hello!');")
```

### 실습 예제 3: 무한 스크롤 크롤링

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def crawl_infinite_scroll(url, scroll_count=5):
    """무한 스크롤 페이지 크롤링 (인스타그램, 페이스북 등)"""
    
    # 드라이버 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # 페이지 열기
        driver.get(url)
        time.sleep(2)
        
        posts = []
        
        # 스크롤 반복
        for i in range(scroll_count):
            print(f"스크롤 {i+1}/{scroll_count}")
            
            # 현재 페이지의 포스트 수집
            elements = driver.find_elements(By.CSS_SELECTOR, '.post-item')
            
            for element in elements:
                try:
                    title = element.find_element(By.CSS_SELECTOR, '.title').text
                    content = element.find_element(By.CSS_SELECTOR, '.content').text
                    
                    posts.append({
                        'title': title,
                        'content': content
                    })
                except:
                    continue
            
            # 페이지 끝까지 스크롤
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 로딩 대기
        
        return posts
        
    finally:
        driver.quit()

# 사용 예시
# posts = crawl_infinite_scroll('https://example.com/feed')
```

### 실습 예제 4: 로그인 후 크롤링

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def crawl_with_login(url, username, password):
    """로그인 후 데이터 크롤링"""
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # 1. 로그인 페이지 접속
        driver.get('https://example.com/login')
        
        # 2. 로그인 정보 입력
        wait = WebDriverWait(driver, 10)
        
        # 아이디 입력
        id_input = wait.until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        id_input.send_keys(username)
        
        # 비밀번호 입력
        pw_input = driver.find_element(By.NAME, 'password')
        pw_input.send_keys(password)
        
        # 3. 로그인 버튼 클릭
        login_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_btn.click()
        
        # 4. 로그인 완료 대기
        wait.until(EC.url_contains('dashboard'))
        
        # 5. 원하는 페이지로 이동
        driver.get(url)
        
        # 6. 데이터 수집
        data = []
        items = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.data-item'))
        )
        
        for item in items:
            data.append(item.text)
        
        return data
        
    finally:
        driver.quit()

# 사용 예시
# data = crawl_with_login('https://example.com/mypage', 'user@email.com', 'password123')
```

### 실습 예제 5: 동적 테이블 크롤링

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def crawl_dynamic_table(url):
    """JavaScript로 생성되는 테이블 크롤링"""
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get(url)
        
        # 테이블 로딩 대기
        wait = WebDriverWait(driver, 10)
        table = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.data-table'))
        )
        
        # 헤더 추출
        headers = []
        header_cells = table.find_elements(By.TAG_NAME, 'th')
        for cell in header_cells:
            headers.append(cell.text)
        
        # 데이터 추출
        data = []
        rows = table.find_elements(By.TAG_NAME, 'tr')[1:]  # 헤더 제외
        
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            row_data = [cell.text for cell in cells]
            data.append(row_data)
        
        # DataFrame 변환
        df = pd.DataFrame(data, columns=headers)
        return df
        
    finally:
        driver.quit()

# 사용 예시
# df = crawl_dynamic_table('https://example.com/table')
# df.to_csv('table_data.csv', index=False, encoding='utf-8-sig')
```

---

## 실전 예제

### 프로젝트 1: 부동산 매물 수집

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

class RealEstateCrawler:
    """부동산 매물 크롤러"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.properties = []
    
    def crawl_page(self, url):
        """한 페이지 크롤링"""
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 매물 목록 추출
        items = soup.select('.property-item')
        
        for item in items:
            try:
                property_data = {
                    'title': item.select_one('.title').text.strip(),
                    'price': item.select_one('.price').text.strip(),
                    'location': item.select_one('.location').text.strip(),
                    'area': item.select_one('.area').text.strip(),
                    'type': item.select_one('.type').text.strip(),
                    'link': item.select_one('a')['href'],
                    'crawled_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.properties.append(property_data)
            except:
                continue
    
    def crawl_multiple_pages(self, base_url, pages=5):
        """여러 페이지 크롤링"""
        for page in range(1, pages + 1):
            print(f"페이지 {page} 크롤링 중...")
            url = f"{base_url}?page={page}"
            self.crawl_page(url)
            time.sleep(1)  # 서버 부담 방지
        
        return pd.DataFrame(self.properties)
    
    def save_to_csv(self, filename='properties.csv'):
        """CSV 저장"""
        df = pd.DataFrame(self.properties)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"{filename}에 {len(df)}개 매물 저장 완료")

# 사용 예시
# crawler = RealEstateCrawler()
# df = crawler.crawl_multiple_pages('https://example-realty.com/list', pages=3)
# crawler.save_to_csv()
```

### 프로젝트 2: SNS 해시태그 분석

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter
import time
import pandas as pd

class HashtagAnalyzer:
    """SNS 해시태그 분석기"""
    
    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.hashtags = []
    
    def scroll_and_collect(self, url, scrolls=10):
        """스크롤하며 해시태그 수집"""
        self.driver.get(url)
        time.sleep(3)
        
        for i in range(scrolls):
            # 포스트 수집
            posts = self.driver.find_elements(By.CSS_SELECTOR, '.post')
            
            for post in posts:
                try:
                    text = post.text
                    # 해시태그 추출 (#으로 시작하는 단어)
                    tags = [word for word in text.split() if word.startswith('#')]
                    self.hashtags.extend(tags)
                except:
                    continue
            
            # 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
    
    def analyze(self, top_n=20):
        """해시태그 분석"""
        counter = Counter(self.hashtags)
        top_tags = counter.most_common(top_n)
        
        df = pd.DataFrame(top_tags, columns=['Hashtag', 'Count'])
        return df
    
    def close(self):
        """드라이버 종료"""
        self.driver.quit()

# 사용 예시
# analyzer = HashtagAnalyzer()
# analyzer.scroll_and_collect('https://example-sns.com/search?q=파이썬', scrolls=5)
# result = analyzer.analyze(top_n=20)
# print(result)
# analyzer.close()
```

---

## 주의사항

### 법적 고려사항

1. **robots.txt 확인**
```python
# https://example.com/robots.txt 확인
import requests

def check_robots_txt(domain):
    """robots.txt 확인"""
    url = f"{domain}/robots.txt"
    response = requests.get(url)
    print(response.text)

check_robots_txt('https://www.naver.com')
```

2. **이용약관 준수**
- 웹사이트의 이용약관 확인
- 크롤링 금지 사이트는 크롤링하지 않기

3. **저작권 존중**
- 수집한 데이터의 상업적 사용 주의
- 출처 표기

### 크롤링 에티켓

```python
import time
import random

# 1. 적절한 대기 시간
time.sleep(random.uniform(1, 3))  # 1~3초 랜덤 대기

# 2. User-Agent 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 3. 요청 빈도 제한
from time import sleep
from datetime import datetime

def rate_limited_request(url, requests_per_minute=10):
    """분당 요청 수 제한"""
    sleep_time = 60 / requests_per_minute
    response = requests.get(url)
    sleep(sleep_time)
    return response
```

### 에러 처리

```python
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

def safe_crawl(url, max_retries=3):
    """안전한 크롤링 (에러 처리)"""
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 4xx, 5xx 에러 발생
            
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
            
        except requests.exceptions.Timeout:
            print(f"타임아웃 발생 (시도 {attempt + 1}/{max_retries})")
            time.sleep(2)
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP 에러: {e}")
            break
            
        except RequestException as e:
            print(f"요청 에러: {e}")
            break
    
    return None

# 사용
soup = safe_crawl('https://example.com')
if soup:
    # 크롤링 작업
    pass
```

---

## 체크리스트

### 크롤링 시작 전
- [ ] 크롤링 목적과 범위 명확히 하기
- [ ] robots.txt 확인
- [ ] 이용약관 검토
- [ ] 정적 vs 동적 페이지 판단
- [ ] 필요한 라이브러리 설치

### 코드 작성 시
- [ ] User-Agent 설정
- [ ] 에러 처리 구현
- [ ] 대기 시간 추가
- [ ] 로깅 구현
- [ ] 데이터 저장 방법 결정

### 실행 후
- [ ] 수집 데이터 검증
- [ ] 중복 제거
- [ ] 데이터 정제
- [ ] CSV/DB 저장
- [ ] 서버 부담 확인

---

## 문제 해결

### Q1: 403 Forbidden 에러
```python
# User-Agent 추가
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.google.com/'
}
```

### Q2: 동적 콘텐츠가 안 보임
```python
# Selenium으로 전환
# 또는 Network 탭에서 API 찾기 (개발자도구 F12)
```

### Q3: 인코딩 깨짐
```python
response.encoding = 'utf-8'
# 또는
response.encoding = response.apparent_encoding
```

### Q4: ChromeDriver 버전 오류
```python
# webdriver-manager 사용 (자동 업데이트)
from webdriver_manager.chrome import ChromeDriverManager
service = Service(ChromeDriverManager().install())
```

---

## 추가 학습 자료

### 공식 문서
- [BeautifulSoup 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium 문서](https://www.selenium.dev/documentation/)
- [requests 문서](https://requests.readthedocs.io/)

### 연습 사이트
- [Books to Scrape](http://books.toscrape.com/) - 크롤링 연습용
- [Quotes to Scrape](http://quotes.toscrape.com/) - 정적 페이지 연습
- [Quotes to Scrape (JS)](http://quotes.toscrape.com/js/) - 동적 페이지 연습

### CSS Selector 학습
- [CSS Diner](https://flukeout.github.io/) - CSS 선택자 게임
- [SelectorGadget](https://selectorgadget.com/) - Chrome 확장 프로그램

---

## 팁 & 트릭

### 1. 개발자 도구 활용 (F12)
```
Elements 탭: HTML 구조 확인
Network 탭: API 요청 확인
Console 탭: JavaScript 테스트
```

### 2. CSS Selector 빠르게 찾기
```
Chrome 개발자 도구에서
요소 우클릭 → Copy → Copy selector
```

### 3. 데이터 저장 형식
```python
# CSV
df.to_csv('data.csv', index=False, encoding='utf-8-sig')

# Excel
df.to_excel('data.xlsx', index=False)

# JSON
import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# SQLite
import sqlite3
conn = sqlite3.connect('data.db')
df.to_sql('table_name', conn, if_exists='replace', index=False)
```

---

**이제 크롤링을 시작하세요!**

```bash
# 간단한 예제로 시작
python
>>> import requests
>>> from bs4 import BeautifulSoup
>>> response = requests.get('http://books.toscrape.com/')
>>> soup = BeautifulSoup(response.text, 'lxml')
>>> titles = soup.select('h3 a')
>>> for title in titles[:5]:
...     print(title.get('title'))
```