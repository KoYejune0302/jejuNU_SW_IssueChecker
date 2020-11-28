from urllib.parse import quote_plus    # 한글 텍스트를 퍼센트 인코딩으로 변환
from selenium import webdriver    # 라이브러리에서 사용하는 모듈만 호출
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException    # 태그가 없는 예외 처리
import time
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

#chrome driver 설정
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome(options=options)

'''
언론사별 10개씩 크롤링
신문사별 oid
경향신문 032
국민일보 005
동아일보 020
문화일보 021
서울신문 081  --> 제외 :  요약 기능 x
세계일보 022
조선일보 023
중앙일보 025
한겨례 028
한국일보 469
'''
OID = ['032','005','020','021','022','023','025','028','469']

from bs4 import BeautifulSoup
import requests
import csv

#날짜 설정
#date = input('날짜를 입력하세요(YYYYMMDD) : ')
OID = ['032','005','020','021','022','023','025','028','469']
date='20201128'

#url저장용 csv 생성
fd = open('url.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(fd)
wr.writerow(['url'])

#언론사 날짜별 뉴스 url 가져오기
for i in range(0,9,1):
    url = "https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid={}&date={}".format(OID[i],date)
    req = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('a',{'class' : 'nclicks(cnt_flashart)'}):
      row=link.get('href')
      temp = [row]
      wr.writerow(temp)

fd.close()

#뉴스기사 저장용 csv 파일 생성
fd = open('output.csv', 'w', encoding='utf-8-sig', newline='')
wr = csv.writer(fd,delimiter=',')
wr.writerow(['Date','Title','Summary'])

#url 읽어오기
url_df = pd.read_csv('url.csv')


#url별로 뉴스 크롤링
for i in range(0,136,1):
    url = url_df.iloc[i,0]
    #selenium
    driver.get(url)
    time.sleep(1)
    try:
        driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div/div[3]/div[2]/div[1]/a').click()
    except :
        print(url)
        continue
    finally:
        time.sleep(5)

        #Beautifulsoup 생성
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #데이터 크롤
        Date = soup.select_one("span.t11")
        Date=str(Date)
        Date=Date[18:]
        Date=Date[:-7]
        Title = soup.find('h3',id="articleTitle")
        Title=str(Title)
        Title=Title[39:]
        Title=Title[:-5]
        Summary = soup.select_one("div._contents_body")
        Summary=str(Summary)
        Summary=Summary[28:]
        Summary=Summary[:-6]

        #csv에 저
        row = []
        row.append(Date)
        row.append(Title)
        row.append(Summary)
        wr.writerow(row)




#csv 닫기
fd.close()

#프로그램 종료
print('finish')
