from bs4 import BeautifulSoup
import requests

url = "https://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=023&aid=0003579434"
req = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
html = req.text
soup = BeautifulSoup(html, 'html.parser')


text_file = open("output.html", "w",encoding='utf-8')
text_file.write(html)
text_file.close()

import csv

fd = open('output.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(fd,delimiter=',')
wr.writerow(['Time','Title','Summary'])

Time = soup.select_one("span.t11")
Title = soup.find('h3',id="articleTitle")
Summary = soup.select_one("div._contents_body")

row = []
row.append(Time)
row.append(Title)
row.append(Summary)
wr.writerow(row)

print(Title)
print(Time)
print(Summary)

fd.close()
