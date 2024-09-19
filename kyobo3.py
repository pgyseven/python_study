from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd
import time
import mariadb
from datetime import datetime

# ChromeDriver 자동 설치
chromedriver_autoinstaller.install()

# Selenium을 사용하여 웹 브라우저 열기
driver = webdriver.Chrome()

# 책 정보를 담을 리스트
books = []

# 크롤링할 페이지 수 설정
num_pages = 15  # 원하는 페이지 수만큼 수정

# 카테고리 코드 범위 설정
category_codes = [
    '050301', '050302', '050303',
    '050501', '050503', '050505',
    '050701', '050703', '050705'
]

# 각 카테고리 코드에 대해 크롤링 수행
for category in category_codes:
    for page in range(1, num_pages + 1):
        # 각 페이지의 URL 생성
        url = f'https://product.kyobobook.co.kr/category/KOR/{category}#?page={page}&type=all&sort=new'
        
        # 해당 페이지로 이동
        driver.get(url)
        
        # 페이지가 완전히 로드될 때까지 대기
        time.sleep(5)  # 5초 대기
        
        # 페이지 소스 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # 책 제목, 이미지, 가격, 저자, 출판사, 발행일, 소개 추출
        for item in soup.find_all('li', class_='prod_item'):
            title_tag = item.find('span', class_='prod_name')
            image_tag = item.find('img', {'data-kbbfn': 's3-image'})
            price_normal_tag = item.find('s', class_='val')
            price_tag = item.find('span', class_='val')
            author_tag = item.find('span', class_='prod_author')
            pubDate_tag = item.find('span', class_='date')
            introduction_tag = item.find('p', class_='prod_introduction')

            # 제목과 이미지 URL 추출
            title = title_tag.get_text(strip=True) if title_tag else ''
            image_url = image_tag['src'] if image_tag else ''
            
            # 가격 정보 추출 및 처리
            price_normal = price_normal_tag.get_text(strip=True).replace('원', '').replace(',', '') if price_normal_tag else ''
            price_sale = price_tag.get_text(strip=True).replace('원', '').replace(',', '') if price_tag else ''
            
            # 저자와 출판사 정보 추출 및 처리
            if author_tag:
                author_info = author_tag.get_text(strip=True).split('·')
                author = author_info[0].strip() if len(author_info) > 0 else ''
                publisher = author_info[1].strip() if len(author_info) > 1 else ''
            else:
                author = ''
                publisher = ''
            
            # 발행일 처리
            if pubDate_tag:
                pubDate_str = pubDate_tag.get_text(strip=True).replace('· ', '').replace('.', '-')
                try:
                    pubDate = datetime.strptime(pubDate_str, '%Y-%m-%d')
                except ValueError:
                    pubDate = None
            else:
                pubDate = None
            
            # 소개 처리
            introduction = introduction_tag.get_text(strip=True) if introduction_tag else ''
            
            # 결과를 딕셔너리로 저장, category도 함께 저장
            books.append({
                'category': category,
                'title': title,
                'image_url': image_url,
                'price_normal': price_normal,
                'price_sale': price_sale,
                'author': author,
                'publisher': publisher,
                'pubDate': pubDate,
                'introduction': introduction,
                'inventory': 30  # 고정 값
            })

# books 리스트 출력
print(books)  # 데이터가 제대로 추출되었는지 확인

# DataFrame으로 변환
df = pd.DataFrame(books, columns=['category', 'title', 'image_url', 'price_normal', 'price_sale', 'author', 'publisher', 'pubDate', 'introduction', 'inventory'])

# DataFrame을 파일로 저장 (선택 사항)
df.to_csv('books.csv', index=False)

# MariaDB 연결 설정
conn = mariadb.connect(
    user="mbcac2024",
    password="academymbc2024**",
    host="mbcac2024.cafe24.com",
    port=3306,
    database="mbcac2024"
)

# 연결 후 문자셋 설정
conn.cursor().execute('SET NAMES utf8mb4;')

# Cursor 생성
cursor = conn.cursor()

# 배치 크기 설정
batch_size = 1000
batch = []

# 데이터 삽입
for book in books:
    batch.append((
        book['title'],
        book['author'],
        book['publisher'],
        book['pubDate'],
        book['category'],  # genre로 사용
        book['price_normal'],
        book['price_sale'],
        book['inventory'],
        book['image_url'],
        book['introduction']
    ))
    
    # 배치 크기 도달 시 삽입
    if len(batch) >= batch_size:
        cursor.executemany('''
            INSERT INTO BookList3 (title, author, publisher, pubDate, genre, price, salePrice, inven, thumbNail, introduction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', batch)
        conn.commit()
        batch = []

# 남은 데이터 삽입
if batch:
    cursor.executemany('''
        INSERT INTO BookList3 (title, author, publisher, pubDate, genre, price, salePrice, inven, thumbNail, introduction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', batch)
    conn.commit()

# 연결 종료
cursor.close()
conn.close()

# 브라우저 닫기
driver.quit()
