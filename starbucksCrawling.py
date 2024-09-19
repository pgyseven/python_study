from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains # 스크롤바 제어
from selenium.webdriver.common.by import By

import requests
import time

import pandas as pd

# 스타벅스의 홈페이지에서 매장의 이름, 주소, 구 이름, 위도, 경도를 크롤링 해와서 csv, DataFrane로 만들기
driver = webdriver.Chrome()
driver.get('https://www.starbucks.co.kr/store/store_map.do')
driver.maximize_window() # 창최대화 반응형의 경우 다를 수 있으니 기준을 잡기위해 최대화
time.sleep(3)

# 모달창 닫기
driver.find_element(By.XPATH, '/html/body/div[4]/p/a').click()
time.sleep(3)

# 지역검색
driver.find_element(By.XPATH, '//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/header[2]/h3/a').click()
time.sleep(2)

# 서울 클릭
driver.find_element(By.XPATH, '//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/article[2]/div[1]/div[2]/ul/li[1]/a').click()
time.sleep(1)

# 전체 클릭
driver.find_element(By.XPATH, '//*[@id="mCSB_2_container"]/ul/li[1]/a').click()
time.sleep(7)

# 전체 매장의 ul
stores = driver.find_element(By.XPATH, '//*[@id="mCSB_3_container"]/ul')
store_list = stores.find_elements(By.TAG_NAME, 'li')
print (len(store_list))

action = ActionChains(driver)

starbucks_list = []

for i in range(0, len(store_list)):
    store = store_list[i]
    action.move_to_element(store).perform() # store 가 가리키는 태그가 보이도록 스크롤바를 움진인다.
    # 매장이름
    name = store.find_element(By.XPATH, '//*[@id="mCSB_3_container"]/ul/li[' + str(i+1) +']/strong').text.strip()
    
    # 주소
    address = store.find_element(By.XPATH, '//*[@id="mCSB_3_container"]/ul/li[' + str(i+1) +']/p').text.strip()
    address = address.replace('1522-3232', '')
    address = address.replace('\n', '')
    
    # 구 이름
    gu = address.split(' ')[1]

    # 위도, 경도
    lat = store.get_attribute('data-lat')
    long = store.get_attribute('data-long')

    # DataFrame으로 만들기 위해 하나의 매장 정보를 Dictionary 로 만듦
    store_info = {
        "브랜드" : "스타벅스",
        "상호명" : name,
        "주소" : address,
        "구" : gu,
        "위도" : lat,
        "경도" : long

    }

    starbucks_list.append(store_info)
    print(store_info)
    print('----------------------------------------------------------------')
df_starbucks = pd.DataFrame(starbucks_list)
print(df_starbucks)

#csv로 저장
df_starbucks.to_csv('starbucks_stores.csv')
    