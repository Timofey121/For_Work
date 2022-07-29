# -*- coding: utf8 -*-
import os
import pickle
import random
import time

from fake_useragent import UserAgent
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from config import login, password, PROXY, login_mamba, password_mamba

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.chrome}")

proxies = {
    # 'https': 'http://proxy_ip:proxy_port'
    'https': f'http://{login}:{password}@{random.choice(PROXY)}'
}
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.mamba.ru/search/list/login")
login_input = driver.find_element(By.NAME, 'login')
login_input.clear()
login_input.send_keys(login_mamba)
time.sleep(2)
password_input = driver.find_element(By.NAME, 'password')
password_input.clear()
password_input.send_keys(password_mamba)
time.sleep(2)
password_input.send_keys(Keys.ENTER)
time.sleep(2)
pickle.dump(driver.get_cookies(), open(f"mamba_cookies", "wb"))
