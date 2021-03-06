import selenium
from selenium import webdriver as wd
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from itertools import repeat
# 크롬드라이버 열기
driver = wd.Chrome() # 크롬드라이버 경로
driver.maximize_window() # 크롬창 크기 최대

# 드라이버가 해당 url 접속
url = 'https://www.melon.com/chart/index.htm' # 멜론차트 페이지
driver.get(url)
# 차트파인더 클릭
driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[1]/li[1]/div/div/button/span').click()

# 연대선택, 연도선택, 월선택, 장르선택

# 월간차트 클릭
driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/h4[2]/a').click()
time.sleep(2)

# 연대선택 2020년 클릭
driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[1]/div[1]/ul/li[1]/span/label').click()
time.sleep(2)

# 연도선택 2021년 클릭
driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[2]/div[1]/ul/li[1]/span/label').click()
time.sleep(2)

# 월선택 11월 클릭
driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[3]/div[1]/ul/li[11]/span/label').click()
time.sleep(2)

# 장르선택 종합 클릭
driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[5]/div[1]/ul/li[1]/span/label').click()
time.sleep(2)

# 검색버튼 클릭
driver.find_element_by_xpath('//*[@id="d_srch_form"]/div[2]/button/span/span').click()

html = driver.page_source # 드라이버 현재 페이지의 html 정보 가져오기
requests.get(url)
soup = BeautifulSoup(html, 'html.parser')

soup.find_all('div', attrs={'class': 'ellipsis rank01'})
[title.find('a').get_text() for title in soup.find_all('div', attrs={'class': 'ellipsis rank01'})]

soup.find_all('span', attrs={'class':'checkEllipsis'})
[ singer.get_text() for singer in soup.find_all('span', attrs={'class':'checkEllipsis'}) ]
song = [title.find('a').get_text() for title in soup.find_all('div', attrs={'class': 'ellipsis rank01'})]

rank = []
for i in range(len(song)):
    rank.append(i+1)
    soup.find_all('span', attrs={'class':'datelk'})
    soup.find_all('span', attrs={'class':'datelk'})[0].get_text() # 년
    soup.find_all('span', attrs={'class':'datelk'})[1].get_text() # 월

period = 1
month = 12
result_df = pd.DataFrame()

while period < 4:
    # 크롬드라이버 열기
    driver = wd.Chrome() # 크롬드라이버 경로
    driver.maximize_window() # 크롬창 크기 최대

    # 드라이버가 해당 url 접속
    url = 'https://www.melon.com/chart/index.htm' # 멜론차트 페이지
    driver.get(url)
    time.sleep(2)

    # 차트파인더 클릭
    driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[1]/li[1]/div/div/button/span').click()
    time.sleep(2)

    # 월간차트 클릭
    driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/h4[2]/a').click()
    time.sleep(2)

    driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[1]/div[1]/ul/li[{}]/span/label'.format(period)).click()
    time.sleep(2)

    # 연도선택(규칙 찾기!)
    driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[2]/div[1]/ul/li[2]/span/label').click()
    time.sleep(2)

    # 월선택 12월 클릭
    driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[3]/div[1]/ul/li[{}]/span/label'.format(month)).click()
    time.sleep(2)

    # 장르선택 종합 클릭
    driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[5]/div[1]/ul/li[1]/span/label').click()
    time.sleep(2)

    # 검색버튼 클릭
    driver.find_element_by_xpath('//*[@id="d_srch_form"]/div[2]/button/span/span').click()
    time.sleep(2)

    # html 정보 가져오기
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 검색 대상이 되는 년도, 월 가져오기
    year = soup.find_all('span', attrs={'class':'datelk'})[0].get_text()
    month = soup.find_all('span', attrs={'class':'datelk'})[1].get_text()

    # 차트의 각 행을 가져오기
    rows = soup.find_all('tr', attrs={'class': 'lst50'})

    ranks = []
    titles = []
    artists = []

    for row in rows:
        ranks.append(row.find('span', attrs={'class': 'rank'}).get_text())
        titles.append(row.find('div', attrs={'class': 'ellipsis rank01'}).get_text())
        artists.append(row.find('div', attrs={'class': 'ellipsis rank02'}).get_text())

    # 데이터프레임 생성
    df = pd.DataFrame({
        '연도': list(repeat(year, len(rows))),
        '월':list(repeat(month, len(rows))),
        '순위': ranks,
        '곡명': titles,
        '가수명': artists
    })
    result_df = pd.concat([result_df, df], ignore_index=True)
    period += 2

result_df.to_csv('롤롤.csv', encoding='utf-8')
