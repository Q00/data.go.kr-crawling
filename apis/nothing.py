from selenium import webdriver
from bs4 import BeautifulSoup
import time

# 지연 함수
#time.sleep(1)

# 접속할 URL
TEST_URL = 'http://smc.skku.edu/smc_main/care/treatSearch.smc'

# 크롬 옵션설정
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')

# Headless 탐지를 회피하기 위한 UserAgent값 변경
options.add_argument("#user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

###     진료과
department_total_list = []
department_total_list2 = []
for global_idx in range(1, 4): #범위지정
    # chromedriver 절대경로 설정
    driver = webdriver.Chrome('C:/Users/HM2/Anaconda3/test1/chromedriver.exe', options=options)

    # URL 접속
    driver.get(TEST_URL)

    # 로딩 3초 대기
    driver.implicitly_wait(3)

    temp_url = '//*[@id="contents"]/form/div/div/ul/li['

    # 진료과 클릭
    xpath_url = temp_url + str(global_idx) + ']'
    # //*[@id="contents"]/form/div/div/ul/li[32] 마지막 항목
    driver.find_element_by_xpath(xpath_url).click()

    department_html = driver.page_source
    department_soup = BeautifulSoup(department_html, 'html.parser')
    department_url_list = department_soup.select('#relation_link a')
    department_url_list2 = department_soup.select('.departments_intro')

    for local_idx, url in enumerate(department_url_list): #진료과명
        if local_idx == global_idx - 1:
            add_list = []
            add_list.append(url.text)
            department_total_list.append(add_list)

    for url2 in department_url_list2: #진료과소개
        add_list2 = []
        add_list2.append(url2.text.replace("\xa0","").replace("\n",""))
        department_total_list2.append(add_list2)
    driver.quit()