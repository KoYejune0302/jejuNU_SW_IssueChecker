from urllib.parse import quote_plus    # 한글 텍스트를 퍼센트 인코딩으로 변환
from selenium import webdriver    # 라이브러리에서 사용하는 모듈만 호출
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException    # 태그가 없는 예외 처리
import time
from bs4 import BeautifulSoup
import requests


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome(options=options)
url='https://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=023&aid=0003579434'
driver.get(url)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div/div[3]/div[2]/div[1]/a').click()
time.sleep(5)
############################################################################################
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


text_file = open("output.html", "w",encoding='utf-8')
text_file.write(html)
text_file.close()

import csv

fd = open('output.csv', 'w', encoding='utf-8-sig', newline='')
wr = csv.writer(fd,delimiter=',')
wr.writerow(['Time','Title','Summary'])

Time = soup.select_one("span.t11")
Time=str(Time)
Time=Time[18:]
Time=Time[:-7]
Title = soup.find('h3',id="articleTitle")
Title=str(Title)
Title=Title[42:]
Title=Title[:-5]
Summary = soup.select_one("div._contents_body")
Summary=str(Summary)
Summary=Summary[28:]
Summary=Summary[:-6]

row = []
row.append(Time)
row.append(Title)
row.append(Summary)
wr.writerow(row)

fd.close()
