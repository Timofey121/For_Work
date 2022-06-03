# -*- coding: utf8 -*-
import os
import pickle
import random
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from Maks_KWORK.y_met.config import login, password, PROXY

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={useragent.chrome}')

proxy_options = {
    'proxy': {
        'http': f'http://{login}:{password}@{PROXY}'
    }
}

ChromeDriver = 'my_chromedriver'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, ChromeDriver)

# options.add_argument("--headless")
with webdriver.Chrome(executable_path=DRIVER_BIN, options=options, seleniumwire_options=proxy_options) as driver:
    driver.get(f'https://passport.yandex.ru/auth/welcome')
    for cookie in pickle.load(open(f"yandex_cookies", "rb")):
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.refresh()
    a = 0
    b = 0
    while a != 1:
        driver.get(f'https://yandex.ru/search/?text=rootracker.ru&lr=51&p={b}')
        time.sleep(20)
        for i in range(len(driver.find_elements(By.CLASS_NAME, 'organic__title-wrapper'))):
            if driver.find_elements(By.CLASS_NAME, 'organic__title-wrapper')[i].get('href') == 'https://roottracker.ru/':
                time.sleep()
                driver.find_elements(By.CLASS_NAME, 'organic__title-wrapper')[i].click()
                a = 1

