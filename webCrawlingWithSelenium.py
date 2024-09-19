# 셀레니움 라이브러리를 이용하여 웹 크롤링을 해 보자.
# 셀레니움은 Selenium WebDriver를 Python으로 wrapping한 library로, 웹 브라우저를 제어할 수 있게 해준다.

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
driver.get("https://www.naver.com/")  

driver.implicitly_wait(10) # 10 초 동안 대기
#shortcutArea > ul > li:nth-child(4) > a > span.service_icon.type_shopping
driver.find_element(By.CSS_SELECTOR, '#shortcutArea > ul > li:nth-child(4) > a > span.service_icon.type_shopping').click()

driver.implicitly_wait(10) 
print(driver.title)

# 쇼핑 페이지가 새로운 탭에서 열렸으므로, 드라이버를 해당 탭으로 전환해야 한다. -1은 맨끝에 창 즉 마지막에 열린창
driver.switch_to.window(driver.window_handles[-1])
print(driver.title)

driver.implicitly_wait(10) 
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/button[2]').click()
driver.implicitly_wait(10) 


# //*[@id="gnb-gnb"]/div[2]/div/div[2]/div/div[2]/form/div[1]/div[1]/input
searchBox = driver.find_element(By.XPATH, '//*[@id="gnb-gnb"]/div[2]/div/div[2]/div/div[2]/form/div[1]/div[1]/input')



searchBox.click()

searchBox.send_keys('아이폰15 pro')
searchBox.send_keys(Keys.ENTER)
driver.implicitly_wait(10) 


