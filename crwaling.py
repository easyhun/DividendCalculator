import requests
import re
from bs4 import BeautifulSoup

codename = ["삼성전자 005930"]
print("코드 목록 : ", codename)

query = input("종목 코드 : ")
url = 'https://finance.naver.com/item/sise.naver?code='+'%s'%query
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

stock_name = soup.select_one('#middle > div.h_company > div.wrap_company > h2 > a').text.strip()
now_val =soup.select_one('#_nowVal').text.replace(',', '')
max52 = soup.select_one('#content > div.section.inner_sub > div:nth-child(1) > table > tbody > tr:nth-child(11) > td:nth-child(2) > span').text.replace(',', '')
min52 = soup.select_one('#content > div.section.inner_sub > div:nth-child(1) > table > tbody > tr:nth-child(11) > td:nth-child(4) > span').text.replace(',', '')

crt_stock = int(re.sub(r'[^0-9]', '', now_val))
imax52 = int(re.sub(r'[^0-9]', '', max52)) #52주 최고가
imin52 = int(re.sub(r'[^0-9]', '', min52)) #52주 최저가
drop_ratio = ((imax52-crt_stock)/imax52) #고점대비 하락율

print(stock_name)
print("현재가 : " + now_val)
print('52주 최저가 : '+ min52)
print('52주 최고가 : '+ max52)
print("고점대비 하락율 : {: .2%}".format(drop_ratio))
