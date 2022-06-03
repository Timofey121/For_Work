# -*- coding: utf8 -*-
import os
import pickle
import random
import time

from fake_useragent import UserAgent
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from Maks_KWORK.vk.config import login, password, PROXY, login_vk, password_vk

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.chrome}")

proxies = {
    # 'https': 'http://proxy_ip:proxy_port'
    'https': f'http://{login}:{password}@{random.choice(PROXY)}'
}

# if platform == "darwin":
#     ChromeDriver = "chromedriver_for_mac"
# elif platform == "linux" or platform == "linux2":
#     ChromeDriver = "chromedriver_for_linux"
# elif platform == "win32" or platform == "win64":
#     ChromeDriver = "my_chromedriver.exe"
# else:
#     print("Для Вашей ОС нет установленных драйверов!")
#     exit(0)

ChromeDriver = "my_chromedriver"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, ChromeDriver)

# options.add_argument("--headless")

with webdriver.Chrome(executable_path=DRIVER_BIN, options=options, seleniumwire_options=proxies) as driver:
    # driver.get(f'https://passport.yandex.ru/auth/welcome')
    # for cookie in pickle.load(open(f"yandex_cookies", "rb")):
    #     driver.add_cookie(cookie)
    # time.sleep(1)
    driver.get("https://m.vk.com/feed")
    login_input = driver.find_element(By.NAME, 'email')
    login_input.clear()
    login_input.send_keys(login_vk)
    time.sleep(2)
    password_input = driver.find_element(By.NAME, 'pass')
    password_input.clear()
    password_input.send_keys(password_vk)
    time.sleep(2)
    password_input.send_keys(Keys.ENTER)
    pickle.dump(driver.get_cookies(), open(f"vk_cookies", "wb"))
