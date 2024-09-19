from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC # 내부에서 웹드라이브 에러처리 그런데 쓰인다.
from selenium.webdriver import ActionChains # 스크롤바 제어
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # 키보드에 키를 제어하기 위해서
import time

import pandas as pd

# 이디아 매장의 매장 이름, 주소를 얻어오자
# 이디아 홈페이지에서는 구 별로 매장 정보를 얻어와야 한다.(전체 검색이 안됨)
# 스타벅스 csv의 구를 참조하여 얻어온다.

df_starbucks = pd.read_csv('starbucks_stores.csv')
setGu = set(df_starbucks['구'].to_list())
print(len(setGu))

for gu in setGu:
    ediyaUrl = 'https://ediya.com/contents/find_store.html#c'
    driver = webdriver.Chrome()
    driver.get(ediyaUrl)
    driver.maximize_window()
    time.sleep(7)

    # 주소
    driver.find_element(By.XPATH, '//*[@id="contentWrap"]/div[3]/div/div[1]/ul/li[2]/a').click()
    time.sleep(2)

    # 주소 검색 -> 검색어를 검색 박스에 입력하고 엔터
    gu = '서울 ' + gu
    driver.find_element(By.XPATH, '//*[@id="keyword"]').send_keys(gu)
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="keyword"]').send_keys(Keys.ENTER)
    time.sleep(5)
    
    ediyaStores = driver.find_element(By.XPATH, '//*[@id="placesList"]')
    ediyaStores = ediyaStores.find_elements(By.TAG_NAME, 'li')

    stores = []
    for store in ediyaStores :
        name = store.text.split('\n')[0]
        address = store.text.split('\n')[1]
        gu = address.split(' ')[1]
        
        storeDict = {
            '브랜드' : '이디야',
            '상호명' : name,
            '구' : gu,
            '주소' : address
        }

        stores.append(storeDict)
        print(storeDict)
        print('===========================================================================================================================')

# DataFrame으로 만들고, csv로 저장
df_ediya = pd.DataFrame(stores)
df_ediya.to_csv('ediya.csv')