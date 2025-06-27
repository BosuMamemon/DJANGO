import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def melon_crawling():
    url = 'https://www.melon.com/chart/index.htm'
    header = {'User-Agent': 'Mozilla/5.0'}

    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')

    tbody = soup.select_one('#frm > div > table > tbody')
    lst50 = tbody.select('tr.lst50')
    top50 = []
    for td in lst50:
        rank = td.select_one('span.rank').get_text()
        title = td.select_one('#lst50 > td:nth-child(6) > div > div > div.ellipsis.rank01 > span > a').get_text()
        singer = td.select_one('#lst50 > td:nth-child(6) > div > div > div.ellipsis.rank02 > a').get_text()
        album = td.select_one('#lst50 > td:nth-child(7) > div > div > div > a').get_text()
        top50.append({
            'rank': rank,
            'title': title,
            'singer': singer,
            'album': album
        })
    return top50

def movie_crawling():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)

    driver.get('https://m.entertain.naver.com/movie')
    driver.implicitly_wait(2)

    box_office = driver.find_element(
        By.XPATH,
        '//*[@id="feed-v2-renderer-root"]/div/div/div[1]/div/div[2]/div/button[1]'
    )
    box_office.send_keys(Keys.ENTER)
    driver.implicitly_wait(2)

    more = driver.find_element(By.XPATH, '//*[@id="feed-v2-renderer-root"]/div/div/div[1]/div/div[4]/button')
    more.send_keys(Keys.ENTER)
    driver.implicitly_wait(2)

    ranking_info = driver.find_elements(
        By.XPATH,
        '//*[@id="feed-v2-renderer-root"]/div/div/div[1]/div/div[3]/ol/li'
    )
    movies = []
    for idx, li in enumerate(ranking_info):
        buttons = li.find_elements(By.CLASS_NAME, 'Home_button_fold__elLFG')
        for button in buttons:
            button.send_keys(Keys.ENTER)
            driver.implicitly_wait(2)
            rank = idx + 1
            title = li.find_element(By.XPATH, './/div/div[1]/a/div[2]').text
            grade = float(li.find_element(By.XPATH, './/div/div[1]/a/div[3]/span[1]/span').text)
            count = li.find_element(By.XPATH, './/div/div[1]/a/div[3]/span[2]').text
            movies.append({'rank': rank, 'title': title, 'grade': grade, 'count': count})

    driver.quit()
    df = pd.DataFrame(movies)
    df.to_csv('static/movies.csv', encoding='utf-8')

    return movies

def movie_chart_crawling():
    df = pd.read_csv('static/movies.csv')
    plt.rcParams['font.family'] = 'Malgun Gothic'

    # 별점
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    df['grade'] = np.floor(df['grade'].astype(float)).astype(int)
    ax1.bar(df['grade'].value_counts().index, df['grade'].value_counts(), color='blue')
    ax1.set_title('네이버 영화 별점 분포')
    ax1.set_xlabel('별점')
    ax1.set_ylabel('영화갯수')

    ax2.pie(df['grade'].value_counts(),
            labels=df['grade'].value_counts().index,
            autopct='%1.1f%%', startangle=90)
    plt.savefig('static/images/movie_grade_chart.png', dpi=300)
    plt.cla()

    # 누적수
    # df['count'] = df['count'].str.split(' ').str[2].str.replace('만명', '').astype(int)
    f, (ax3, ax4) = plt.subplots(1, 2, figsize=(10, 5))
    df['count'] = df['count'].str.split(' ').str[2].str.extract(r'(\d+)').astype(int)
    ax3.bar(df['count'].value_counts().index, df['count'].value_counts(), color='green')
    ax3.set_title('네이버 영화 누적 관객수 분포')
    ax3.set_xlabel('누적 관객수')
    ax3.set_ylabel('영화갯수')
    ax4.pie(df['count'].value_counts(),
            labels=df['count'].value_counts().index,
            autopct='%1.1f%%', startangle=90)
    plt.savefig('static/images/movie_count_chart.png', dpi=300)
    plt.cla()

    # 누적 관객수가 20만명을 넘는 것만 파이 그래프 출력
    f, (ax5, ax6) = plt.subplots(1, 2, figsize=(10, 5))
    df_filtered = df[df['count']>=20].copy()
    ax5.bar(df_filtered['count'].value_counts().index, df_filtered['count'].value_counts(), color='green')
    ax5.set_title('누적 관객수 20만명 이상 영화 분포')
    ax5.set_xlabel('누적 관객수')
    ax5.set_ylabel('영화갯수')
    ax6.pie(df_filtered['count'].value_counts(),
            labels=df_filtered['count'].value_counts().index,
            autopct='%1.1f%%', startangle=90)
    plt.savefig('static/images/movie_count_20.png', dpi=300)
    plt.cla()

    image_dic = {
        'grade_chart': '/static/images/movie_grade_chart.png',
        'count_chart': '/static/images/movie_count_chart.png',
        "count_20": '/static/images/movie_count_20.png'
    }
    return image_dic

def starbucks():
    result = []

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.starbucks.co.kr/store/store_map.do")
    driver.implicitly_wait(10)
    driver.find_element(By.LINK_TEXT, "지역 검색").send_keys(Keys.ENTER)
    driver.implicitly_wait(10)
    driver.find_element(By.LINK_TEXT, "부산").send_keys(Keys.ENTER)
    driver.implicitly_wait(10)
    driver.find_element(By.LINK_TEXT, "전체").send_keys(Keys.ENTER)
    driver.implicitly_wait(60)

    # 크롤링
    driver.execute_script("document.querySelector('#mCSB_3').style.cssText = 'overflow: visible;'")
    ul_tag = driver.find_element(By.CLASS_NAME, "quickSearchResultBoxSidoGugun")
    store_list = ul_tag.find_elements(By.TAG_NAME, "li")
    for store in store_list:
        name = store.get_attribute("data-name")
        addressAndTel = store.find_element(By.CSS_SELECTOR, "p").text.split("\n")
        address = addressAndTel[0]
        tel = addressAndTel[1]
        latitude = store.get_attribute("data-lat")
        longtitude = store.get_attribute("data-long")
        result.append({
            'name': name,
            'address': address,
            'tel': tel,
            'latitude': latitude,
            'longtitude': longtitude
        })

    driver.quit()

    return result