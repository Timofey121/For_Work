# -*- coding: utf8 -*-
import datetime
import pickle
import random
import time

import pymysql
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from config import login, password, PROXY

con = pymysql.connect(host="",
                      user="",
                      passwd="",
                      database='',
                      )

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={useragent.chrome}')

proxies = {'https': f'http://{login}:{password}@{random.choice(PROXY)}'}

categories = ['koronavirus', 'politics', 'society', 'business', 'world', 'incident', 'culture',
              'computers', 'science', 'auto']
normal_cat = ['Interesting', 'Coronavirus', 'Politics', 'Society', 'Business', 'In the World', 'Sports', 'Culture',
              'Technology', 'Science', 'Auto']
amount = 20
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(f'https://passport.yandex.ru/auth/welcome')
for cookie in pickle.load(open(f"yandex_cookies", "rb")):
    driver.add_cookie(cookie)
time.sleep(1)
for item in categories:
    driver.get(f'https://yandex.ru/news/rubric/{item}')
    try:
        for i in range(10):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
    except:
        time.sleep(60)
        for i in range(10):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
    for i in range(1, amount + 1):
        try:
            cat = f"{item}"
            name_state = soup.find_all(class_='mg-grid__col')[i].find(class_='mg-card__title').text
            source = soup.find_all(class_='mg-grid__col')[i].find(class_='mg-card-source__source').find('a').text
            b = soup.find_all(class_='mg-grid__col')[i].find(class_='mg-card-source__time').text
            time_post = f'{datetime.datetime.today().strftime("%Y.%m.%d")} {b}'
            a = '"'
            try:
                photo = soup.find_all(class_='mg-grid__col')[i].find(class_='mg-card-media__image').find('img').get(
                    'src')
            except:
                photo = list(
                    soup.find_all(class_='mg-grid__col')[i].find(class_='mg-card__media-block_type_image').get(
                        'style').split('url(')[-1])
                del photo[-1]
                photo = ''.join(photo)
            # print(f'{soup.find_all(class_="mg-grid__col")[i].find(class_="mg-card__title").find("a").get("href")}')
            ur = soup.find_all(class_='mg-grid__col')[i].find('a').get('href')
            driver.get(f'{ur}')
            soup1 = BeautifulSoup(driver.page_source, 'lxml')
            link = soup1.find(class_='mg-story__title-link').get('href')
            try:
                desc = soup1.find_all('span', class_='mg-snippet__text')
            except:
                desc = soup1.find('span', class_='mg-snippet__text')
            desc1 = []
            for d in range(len(desc)):
                for j in range(len(desc[d].find_all('span'))):
                    desc1.append(desc[d].find_all('span')[j].text)
            photo_1 = photo.replace(f'{a}', '').replace(')', '')
            cur = con.cursor()
            cur.execute(
                f"INSERT INTO news (cat, name, source_name, date, source_link, img, full_desc, user_id)  VALUES ('{normal_cat[categories.index(item)]}', '{name_state}', '{source}', '{time_post}', '{link}', '{photo_1}', '{''.join(desc1)}', 6)")
            con.commit()
        except Exception as ex:
            pass
    # time.sleep(40)
