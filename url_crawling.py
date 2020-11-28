from bs4 import BeautifulSoup
import requests
import csv

#date = input('날짜를 입력하세요(YYYYMMDD) : ')
OID = ['032','005','020','021','022','023','025','028','469']
date='20201128'

fd = open('url.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(fd)
wr.writerow(['url'])

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
print('finish')
