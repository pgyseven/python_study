import requests
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd
import mariadb
import sys
import time



# ChromeDriver 자동 설치
chromedriver_autoinstaller.install()


try:
    conn = mariadb.connect(
        user="mbcac2024",
        password="academymbc2024**",
        host="mbcac2024.cafe24.com",
        port=3306,
        database="mbcac2024"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


def insertProduct(productDict) :
    # connection 객체 생성
    try:
        conn = mariadb.connect(
            user="mbcac2024",
            password="academymbc2024**",
            host="mbcac2024.cafe24.com",
            port=3306,
            database="mbcac2024"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

# Get Cursor
    # cursor 객체 생성(query문을 db에 전송하여 실행 시키고, 결과를 받아오는 역할의 객체)
    cursor = conn.cursor()
    # insertProduct() SQL query
    print(productDict)
    query = "insert into BookList1(title, author, publisher, pubDate , genre, price , salePrice , inven , thumbNail) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"; # %s : parameter placeholder
    # query 실행
    try :
        for i in range(len(productDict)):
            cursor.execute(query,(productDict['title'][i],productDict['author'][i],productDict['publisher'][i], productDict['pubDate'][i], productDict['genre'][i], productDict['price'][i], productDict['salePrice'][i], 30, productDict['thumbnail'][i]))
    except Exception as e :
        print('insert error : ' , e)
    else :
        print('insert success')
        conn.commit()
    # db close
    cursor.close()
    conn.close()







# Selenium을 사용하여 웹 페이지 열기
driver = webdriver.Chrome()
for cat in range(1,11,2) :
    if(cat<10) :
        cat = '0'+str(cat)
    elif(cat>=10) :
        cat = str(cat)
        if(cat == 33) :
            continue
    driver.implicitly_wait(15) # 10초 동안 대기
    time.sleep(1)
    for page in range(1, 11) :
        driver.get('https://product.kyobobook.co.kr/category/KOR/0505'+str(cat)+'#?page='+str(page)+'&type=all&per=20&sort=new')
        driver.implicitly_wait(15) # 10초 동안 대기
        # 페이지 소스 가져오기
        html = driver.page_source
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')

        # 책 정보를 담을 리스트
        books = []

        # 책 제목, 이미지, 가격 추출
        for item in soup.find_all('li', class_='prod_item'):  # 'prod_item' 클래스 확인
            title_tag = item.find('span', class_='prod_name')
            driver.implicitly_wait(1) # 10초 동안 대기
            image_tag = item.find('img', {'data-kbbfn': 's3-image'})
            sale_price_tag = item.find('span', class_='val')
            price_tag = item.find('s', class_='val')
            author_tag = item.find('span', class_='prod_author') # 작성자와 출판사가 같이나옴...
            pubDate_tag = item.find('span', class_='date')
            snb_title = soup.find('a', class_='snb_title') # 장르는 임의로 넣기
            
            
            if title_tag and image_tag and sale_price_tag and price_tag:
                title = title_tag.get_text(strip=True)
                image_url = image_tag['src']
                price = price_tag.get_text(strip=True).replace('원', '').replace(',', '')
                sale_price = sale_price_tag.get_text(strip=True).replace('원', '').replace(',', '')
                author =author_tag.get_text(strip=True).split('·')[0].replace(' ','') # 작성자와 출판사가 같이나옴...
                publisher =author_tag.get_text(strip=True).split('·')[1].replace(' ','') # 작성자와 출판사가 같이나옴...
                pubDate =pubDate_tag.get_text(strip=True).replace('· ','').replace('.','-') # 작성자와 출판사가 같이나옴...
                genre =snb_title.get_text(strip=True) # 작성자와 출판사가 같이나옴...
                
                # 결과를 딕셔너리로 저장
                books.append({
                    'title': title,
                    'thumbnail': image_url,
                    'price': price ,
                    'salePrice': sale_price ,
                    'author': author ,
                    'publisher': publisher ,
                    'pubDate': pubDate ,
                    'genre': genre 
                })

        # books 리스트 출력
        print(books)  # 데이터가 제대로 추출되었는지 확인

        # DataFrame으로 변환
        df = pd.DataFrame(books, columns=['title', 'thumbnail', 'price','author','pubDate','genre','salePrice','publisher'])

        # 추출한 책 정보 출력
        for book in books:
            print(f"Title: {book['title']}")
            print(f"thumbnail: {book['thumbnail']}")
            print(f"Price: {book['price']}")
            print(f"salePrice: {book['salePrice']}")
            print(f"author: {book['author']}")
            print(f"publisher: {book['publisher']}")
            print(f"pubDate: {book['pubDate']}")
            print(f"genre: {book['genre']}")
            print('-' * 40)
        insertProduct(df)
        # 브라우저 닫기
# driver.quit()