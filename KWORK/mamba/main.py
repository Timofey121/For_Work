# -*- coding: utf8 -*-
import os
import pickle
import random
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from Maks_KWORK.mamba.config import login, password, PROXY

if not os.path.isfile('girl_mamba'):
    f = open("girl_mamba", "x")
    f.close()

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.chrome}")

proxies = {
    # 'https': 'http://proxy_ip:proxy_port'
    'https': f'http://{login}:{password}@{random.choice(PROXY)}'
}

fraze = "Привет, знаешь что самое главное в жизни мужчины?"

ChromeDriver = "my_chromedriver"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, ChromeDriver)

# options.add_argument("--headless")

with webdriver.Chrome(executable_path=DRIVER_BIN, options=options, seleniumwire_options=proxies) as driver:
    driver.get("https://www.mamba.ru/search/list/login")
    for cookie in pickle.load(open(f"mamba_cookies", "rb")):
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.refresh()
    driver.get("https://www.mamba.ru/search/list")
    time.sleep(3)
    for i in range(11):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "lxml")
    girls = soup.find_all("div", class_="sc-1pkcrix-16")
    with open("girl_mamba", encoding="utf-8") as f:
        a = f.read()
    a = a.strip().split('\n')
    for i in range(len(girls)):
        try:
            if girls[i].find("a").get("href").split("/")[2] != 'list' and girls[i].find("a").get("href").split("/")[
                2] not in a:
                driver.get(f'https://www.mamba.ru/chats/{girls[i].find("a").get("href").split("/")[2]}/contact')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                text_send = driver.find_element(By.XPATH,
                                                '//*[@id="app-wrapper"]/div[4]/div/div[2]/div/div/div[4]/div[2]/div/div[2]/div/textarea')
                text_send.send_keys(fraze)
                driver.find_element(By.CLASS_NAME, "ftgBUz").click()
                with open("girl_mamba", 'a', encoding="utf-8") as f:
                    f.write(f'{girls[i].find("a").get("href").split("/")[2]}\n')
                time.sleep(40)
                print(f'Написал девушке с id = {girls[i].find("a").get("href").split("/")[2]}')
            else:
                if girls[i].find("a").get("href").split("/")[2] in a:
                    print(f'Уже писали девушке с id = {girls[i].find("a").get("href").split("/")[2]}')
        except Exception as ex:
            pass
print("Успешно!")
