#  웹 크롤링 : web page 에서 원하는 정보(text, image, video)를 가져와서 수집하는 것
# 웹 크롤링을 할 때 저작권 문제가 될 수 있으니, 원래의 상태의 데이터를 가공하여 사용하는 것이 좋다.
# www.lemite.com 크롤링 하겠다 단순한 페이지로
# 파이썬에서 웹 크롤링 할때 필수 유명 라이브러리 : beautyfulsoup4, selenium이 있다.
# beautifulsoup4 은 정적인 페이지를 크롤링 할 때 편하게 사용할 수 있다.
# selenium 은 동적인 페이지를 크롤링할 때 , 사용할 수 있다.

import requests
from bs4 import BeautifulSoup # bs4 패키지에서 BeautifulSoup 클래스를 import
import pymysql

def selectAllProduct():
    # connection 객체 생성
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pgy', charset='utf8')
    # cursor 객체 생성(quert문을 db에 전송하여 실행시키고, 결과를 받아오는 역할의 객체)
    cursor = conn.cursor()
    # selectAllProduct query
    query = "SELECT * FROM lemiteproducts"
    # query 실행
    cursor.execute(query)
    # 위의 쿼리문은 row 가 여러개 이므로, query 결과를 fetchall() 로 fetch
    result = cursor.fetchall()
    #db close
    cursor.close()
    conn.close()
    for product in result:
        print(product)

    
    

def selectProductByProductNo(productNo):
    # connection 객체 생성
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pgy', charset='utf8')
    # cursor 객체 생성(quert문을 db에 전송하여 실행시키고, 결과를 받아오는 역할의 객체)
    cursor = conn.cursor()
    # selectAllProduct query
    query = "SELECT count(*) FROM lemiteproducts where productNo = %s" % (productNo)
    # query 실행
    cursor.execute(query)
    # 위의 쿼리문은 row 가 한개 이므로, query 결과를 fetchall() 로 fetch
    result = cursor.fetchone()
    #db close
    cursor.close()
    conn.close()
    
    return result[0]

def insertProduct(productDict) :
    # connection 객체 생성
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pgy', charset='utf8', port=3306)
    # cursor 객체 생성(query문을 db에 전송하여 실행 시키고, 결과를 받아오는 역할의 객체)
    cursor = conn.cursor()
    # insertProduct() SQL query
    query = "insert into lemiteproducts values(%s, %s, %s, %s, %s)" 
    # query 실행
    try :
        cursor.execute(query, (productDict['prodNo'], productDict['prodName'], productDict['price'], productDict['thumbNail'], productDict['detailUrl']))
    except Exception as e :
        print('insert error : ' , e)
    else :
        print('insert success')
        conn.commit()
     
    # db close
    cursor.close()
    conn.close()
    


def updateProduct(productDict) :
    # connection 객체 생성
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pgy', charset='utf8', port=3306)
    # cursor 객체 생성(query문을 db에 전송하여 실행 시키고, 결과를 받아오는 역할의 객체)
    cursor = conn.cursor()
    # update SQL query
    query = "update lemiteproducts set productName = %s, price = %s, thumbNail = %s, detailUrl = %s WHERE productNo = %s" 
    # query 실행
    try :
        cursor.execute(query, (productDict['prodName'], productDict['price'], productDict['thumbNail'], productDict['detailUrl'], productDict['prodNo']))
    except Exception as e :
        print('update error : ' , e)
    else :
        print('update success')
        conn.commit()
    
    # db close
    cursor.close()
    conn.close()



def deleteProduct(productNo) :
    # connection 객체 생성
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pgy', charset='utf8', port=3306)
    # cursor 객체 생성(query문을 db에 전송하여 실행 시키고, 결과를 받아오는 역할의 객체)
    cursor = conn.cursor()
    # update SQL query
    query = "delete from lemiteproducts where productNo = %s" 
    # query 실행
    try :
        cursor.execute(query, productNo)
    except Exception as e :
        print('delete error : ' , e)
    else :
        print('delete success')
        conn.commit()
    
    # db close
    cursor.close()
    conn.close()




for i in range(1, 3): #  page 포함, 미만
    targetUrl = 'https://www.lemite.com/product/list.html?cate_no=43&page=' + str(i) # url page number

    headers = {'User-Agent': 'Mozilla/5.0'} # 크롭 웹르라우저의  user-agent에 붙여서 request를 보내려고
    responese = requests.get(targetUrl, headers=headers)
    responese.encoding = 'utf-8'
    html = responese.text

    if html is not None:
        html = BeautifulSoup(html, 'html.parser') # html을 parsing 돔태그로 바꿔준거임 html 돔 구조가 되는거 임
        
        # prdList column4
        try : # 이거 해봐라
            products = html.find('ul', {'class': 'prdList column4'})
        except : # 예외가 발생 했다면
            print('Error : product not found')
        else : # 예외가 발생하지 않았다면
            #print(products)
            products = products.find_all('li', {'class': 'item xans-record-'}) 

            for product in products:
                #print(product)
                productDict = {}
                # 상품명
                productDict['prodName'] = product.find('p', {'class' : 'name'}).text.split(':')[1].strip() # product name strip() 앞뒤 공백 제거
                
                # 썸네일 이미지
                thumbImg = product.find('img', {'class' : 'thumb'}).attrs['src']
                if thumbImg.startswith('//'):
                    thumbImg = 'https:' + thumbImg
        
                productDict['thumbNail'] = thumbImg
                #productDict['thumbNail'] ='https:' + product.find('img',{'class' : 'thumb'}).attrs['src'] 
                
                # 상품번호
                productDict['prodNo'] = product.attrs['id'].split('_')[1].strip()

                # 판매가
                productDict['price'] = product.find('li', {'class' : 'xans-record-'}).next_sibling.next_sibling.text.split(':')[1].replace(',','').replace('원','').strip() #  xans-record- 여기서 클래스명에 공백이 있어도 공백을 빼야한다  

                # 상세페이지
                productDict['detailUrl'] = 'https://www.lemite.com/' + product.find('p', {'class' : 'name'}).find('a').attrs['href']
                #detailResponse = requests.get(detailUrl, headers=headers)
                #detailResponse.encoding = 'utf-8'
                #detailHtml = dettailResponse.text


                # 할인가
                #print(product.find('li', {'class' : 'xans-record-'}).next_sibling.next_sibling.next_sibling.next_sibling.text)

                #print(productDict)
                #print(detailHtml)
                # detailHtml = BeautifulSoup(detailHtml, 'html.parser')
                # 원하는 정보 크롤링

                
                #print(productDict)
                
                print('---------------------------------------------------------------------------')
                


                # MySQL DB 에 insert
                # conn = pymysql.connect(host='localhost', user='root', password='password', db='web_crawling', charset='utf8')
                # cursor = conn.cursor()
                # sql = '''
                # INSERT INTO lemite_products (prod_name, thumb_nail, prod_no, price, detail_url)
                # VALUES (%s, %s, %s, %s, %s)
                # '''
                # cursor.execute(sql, (productDict['prodName'], productDict['thumbNail'], productDict['prodNo'], productDict['price'], detailUrl))
                # conn.commit()
                # cursor.close()
                # conn.close()

                #selectAllProduct() # 전체 product 조회
                # db 에 크롤링 한 상품들을 insert(pk가 없을 경우) or update(pk가 있을 경우)
                if selectProductByProductNo(productDict['prodNo'])  != 0 : # 괄호 안에 내 db 에 있는 컬럼의 번호
                    print('상품이 존재한다. > update')
                    updateProduct(productDict)
                else :
                    print('상품이 존재하지 않다. > insert ')
                    insertProduct(productDict)

#deleteProduct(62600) # id 1번 product delete