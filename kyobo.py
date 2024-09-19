import requests
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd

# ChromeDriver 자동 설치
chromedriver_autoinstaller.install()

# Selenium을 사용하여 웹 페이지 열기
driver = webdriver.Chrome()
driver.get('https://product.kyobobook.co.kr/category/KOR/050301?page=1&type=all&sort=new')

# 페이지 소스 가져오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 책 정보를 담을 리스트
books = []

# 책 제목, 이미지, 가격 추출
for item in soup.find_all('li', class_='prod_item'):  # 'prod_item' 클래스 확인
    title_tag = item.find('span', class_='prod_name')
    image_tag = item.find('img', {'data-kbbfn': 's3-image'})
    price_tag = item.find('span', class_='val')
    
    if title_tag and image_tag and price_tag:
        title = title_tag.get_text(strip=True)
        image_url = image_tag['src']
        price = price_tag.get_text(strip=True)
        
        # 결과를 딕셔너리로 저장
        books.append({
            'title': title,
            'image_url': image_url,
            'price': price
        })

# books 리스트 출력
print(books)  # 데이터가 제대로 추출되었는지 확인

# DataFrame으로 변환
df = pd.DataFrame(books, columns=['title', 'image_url', 'price'])

# 추출한 책 정보 출력
for book in books:
    print(f"Title: {book['title']}")
    print(f"Image URL: {book['image_url']}")
    print(f"Price: {book['price']}")
    print('-' * 40)

# 브라우저 닫기
driver.quit()