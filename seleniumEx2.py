# 셀레니움을 이용하여
# https://ncov.kdca.go.kr/pot/index.do 사이트로 이동한 후
# 감염병 주요뉴스 메뉴를 클릭하게 하고
# 뉴스에 "확진자" 검색 후 나오는 게시글의 제목을 추출하여 list에 넣으시고, 출력하세요

from selenium import webdriver
# 크롬에 옵션을 주는 클래스
from selenium.webdriver.chrome.options import Options

# 웹브라우저를 실제 구동 시키는 객체임
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

# 크롬 웹 브라우저의 driver를 자동 업데이트 크롬도 매번 업데이트 되니깐~
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 실험 옵션을 추가 / 크롬 웹 브라우저 꺼짐 방지
chrome_options.add_argument("--start-maximized")  # 크롬 웹 브라우저 최대화 사이즈 줄이면 반응형이라 태그 값도 달라지고 할 수도 있어서

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 해당 웹 주소로 이동
driver.get("https://ncov.kdca.go.kr/pot/index.do")  

driver.implicitly_wait(10) # 10 초 동안 대기



# 감염병 주요뉴스 메뉴를 클릭하게 하고
driver.find_element(By.XPATH, '//*[@id="gnb"]/div/ul/li[2]/a').click()
driver.implicitly_wait(10)


driver.find_element(By.XPATH, '//*[@id="modal-menu"]/div[1]/div[2]/div[2]/ul/li[1]/a').click()
driver.implicitly_wait(10)

searchBox = driver.find_element(By.XPATH, '//*[@id="q_searchVal"]')
searchBox.click()
searchBox.send_keys('확진자')
searchBox.send_keys(Keys.ENTER)
driver.implicitly_wait(10) 

for i in range(1, 11):
    # 뉴스에 "확진자" 검색 후 나오는 게시글의 제목을 추출하여 list에 넣으시고, 출력하세요
    titles={}
    titles[i] = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/table/tbody/tr['+str(i)+']/td[2]/a').get_property('innerText')
    print(titles)
driver.find_element(By.XPATH, '//*[@id="modal-menu"]/div[1]/div[2]/div[2]/ul/li[1]/a').click()

# 강사님 버전
# 감염병 주요뉴스 클릭
driver.find_element(By.XPATH, '//*[@id="tab_list"]/ul/li[1]/ul/li/div/a[1]').click()
driver.implicitly_wait(20) 
driver.find_element(By.CSS_SELECTOR, '#content > div > div.pagenation > a.next-page').click()


# 뉴스 검색
# search = driver.find_element(By.CSS_SELECTOR, '#q_searchVal')
# search.send_keys("확진자")
# search.send_keys(Keys.ENTER)

# 뉴스 제목 추출
titles = driver.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/table/tbody/tr[1]/td[2]/a')

print(titles.text)
#content > div > div.table-board.mt50 > table > tbody > tr:nth-child(2) > td.cell-subject > a

#content > div > div.table-board.mt50 > table > tbody > tr:nth-child(1) > td.cell-subject > a

for i in range(1, 11) :
  titles = driver.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/table/tbody/tr['+str(i)+']/td[2]/a')
  print(titles.text)