# -*- coding: utf8 -*-
import os
import random
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from Maks_KWORK.vk.config import login, password, PROXY

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.chrome}")

proxies = {
    'https': f'http://{login}:{password}@{random.choice(PROXY)}'
}
ChromeDriver = "my_chromedriver.exe"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, ChromeDriver)

# options.add_argument("--headless")

with webdriver.Chrome(executable_path=DRIVER_BIN, options=options, seleniumwire_options=proxies) as driver:
    driver.get("https://passport.yandex.ru/registration")
    driver.find_element(By.ID, 'firstname').send_keys("Тимофей")
    driver.find_element(By.ID, 'lastname').send_keys("Юртаев")
    driver.find_element(By.ID, 'login').send_keys("iurtaev.t")
    driver.find_element(By.ID, 'password').send_keys("Password12345687")
    driver.find_element(By.ID, 'password_confirm').send_keys("Password12345687")
    driver.find_elements(By.CLASS_NAME, 'Link_pseudo')[-1].click()
    time.sleep(30000)

