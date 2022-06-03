# -*- coding: utf8 -*-
import os
import pickle
import random
import string
import time

import mysql.connector
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from textblob import TextBlob

if not os.path.isfile('people_vk'):
    f = open("people_vk", "x")
    f.close()

cyan = '\033[96m'
useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.chrome}")


def fert():
    f = open('vk.txt').read().split('\n')[0].split(';')
    login_vk = str(f[0])
    password_vk = str(f[1])
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent.chrome}")

    drtyu = open('proxy.txt').read().split('\n')[0].split(';')
    PROXY = str(drtyu[0])
    login = str(drtyu[1])
    password = str(drtyu[-1])

    proxies = {
        'proxy': {
            'http': f'http://{login}:{password}@{PROXY}'
        }
    }

    ChromeDriver = "my_chromedriver"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, ChromeDriver)

    # options.add_argument("--headless")

    with webdriver.Chrome(executable_path=DRIVER_BIN, options=options, seleniumwire_options=proxies) as driver:
        # driver.get(f'https://passport.yandex.ru/auth/welcome')
        # for cookie in pickle.load(open(f"vk_cookies", "rb")):
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


if os.path.exists('yandex_cookies') is not True:
    fert()

drtyu = open('proxy.txt').read().split('\n')[0].split(';')
PROXY = str(drtyu[0])
login = str(drtyu[1])
password = str(drtyu[-1])
proxies = {
    'proxy': {
        'http': f'http://{login}:{password}@{PROXY}'
    }
}

ChromeDriver = "my_chromedriver"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, ChromeDriver)

# options.add_argument("--headless") # раскоментировали - браузер вылезает, иначе нет

with webdriver.Chrome(executable_path=DRIVER_BIN, options=options, seleniumwire_options=proxies) as driver:
    driver.get("https://m.vk.com/feed")
    for cookie in pickle.load(open(f"vk_cookies", "rb")):
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.refresh()
    name_people = "Наташа"
    from_wich_age = "15"
    to_which_age = "18"
    line = f"https://m.vk.com/search?c%5Bq%5D={name_people}&c%5Bname%5Bage_from%5D={from_wich_age}&c%5Bage_from%5D={from_wich_age}&c%5Bage_to%5D={to_which_age}"
    driver.get(line)
    for i in range(10):  # чем больше range(x) - больше людям напишет
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        print("Скролю")
    soup = BeautifulSoup(driver.page_source, "lxml")
    items = soup.find_all(class_='simple_fit_item')
    for i in range(len(items)):
        defrt = 0
        try:
            name_girl = items[i].find('span', class_='si_owner').text
            href_girl = f"https://m.vk.com{items[i].get('href')}"
            location_girl = items[i].find_all('div', class_='si_slabel')[0].text
            year_girl = items[i].find_all('div', class_='si_slabel')[1].text
            driver.get(url=href_girl)
            time.sleep(3)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            soup_1 = BeautifulSoup(driver.page_source, "lxml")
            for rt in range(len(soup_1.find_all(class_='Btn_theme_regular'))):
                id = str(soup_1.find_all(class_='Btn_theme_regular')[rt].get('href'))
                if 'write' in id and '?mvk_entrypoint=profile_page' in id:
                    id = id.split("/write")[-1].replace('?mvk_entrypoint=profile_page', '')
                    break
            with open("people_vk", encoding="utf-8") as f:
                file = f.read()
            file = file.strip().split('\n')
            if str(id) not in file:
                req = requests.get(url=f"{href_girl}?act=info")
                soup_2 = BeautifulSoup(req.text, "lxml")
                happy_birth = soup_2.find_all(class_="OwnerInfo__rowCenter")[-2].text
                if len(soup_1.find_all(class_="thumb_map_img_as_div")) < 5:
                    bac = len(soup_1.find_all(class_="thumb_map_img_as_div"))
                else:
                    bac = 5
                photo = []
                # print(soup_1)
                for j in range(bac):
                    try:
                        ph = soup_1.find_all(class_="thumb_map_img_as_div")[j].get("data-src_big")
                        photo.append(ph)
                    except:
                        pass
                try:
                    vk_page = f"https://m.vk.com/write{id}?mvk_entrypoint=profile_page"
                    driver.get(f"https://m.vk.com/write{id}?mvk_entrypoint=profile_page")
                    try:
                        letters = string.ascii_lowercase
                        rand_string = ''.join(random.choice(letters) for i in range(16))
                        login_mamba_2 = f"{TextBlob(str(name_girl.split(' ')[0]).lower()).translate(to='en')}_{TextBlob(str(name_girl.split(' ')[-1]).upper()).translate(to='en')}"
                        driver.find_element(By.NAME, "message").send_keys(
                            f"Привет. Мужчина просит поделиться видео про телегонию. Он выглядит честным, решила ему помочь.. Жаль что сама не знала.... https://www.youtube.com/watch?v=cbouKZeIFkw")
                        # f"Он выглядит честным, решила ему помочь.. Жаль что сама не знала...."
                        # f"https://www.youtube.com/watch?v=cbouKZeIFkw")
                        # driver.find_element(By.CLASS_NAME, "uMailWrite__buttonSend_sendActive").click()
                        driver.find_element(By.ID, "write_submit").click()  # раскоментировали - отправили сообщение

                        con = mysql.connector.connect(
                            host="192.168.1.3",
                            user="roottracker",
                            passwd="31753701RootTracker22",
                            database="roottracker")
                        cur = con.cursor()
                        cur.execute(
                            f"INSERT INTO test_users (fullname, login, passw, vk_page, vk_id, lowPhotoUrl, originPhotoUrl, normalPhotoUrl, bigPhotoUrl) VALUES ('{name_girl}', '{login_mamba_2}', '{rand_string}', '{href_girl}', '{id}', '{photo[0]}', '{photo[0]}', '{photo[0]}', '{photo[0]}')")
                        con.commit()
                        del photo[0]
                        cur.execute(f"select id from test_users where vk_id = '{id}'")
                        rows = cur.fetchall()
                        for row in rows:
                            a = row[0]
                        for t in range(len(photo)):
                            cur.execute(
                                f"INSERT INTO test_photos (fromUserId, originImgUrl) VALUES ('{a}', '{photo[t]}')")
                            con.commit()
                        with open("people_vk", 'a', encoding="utf-8") as f:
                            f.write(f"{id}\n")
                        print(f"Написал девушке с id = {id}")
                    except Exception as ex:
                        print(ex)
                except Exception as ex:
                    pass
            else:
                if str(id) in file:
                    print(f"Уже писали человеку с id = {id}")
        except Exception as ex:
            pass

        if defrt < 5 and defrt != 0:
            f = open('vk.txt').read().split('\n')
            del f[0]
            file_outpput = open('vk.txt')
            os.remove('vk_cookies')
            print(f, file=file_outpput)
            f = open('proxy.txt').read().split('\n')
            del f[0]
            file_outpput = open('proxy.txt')
            print(f, file=file_outpput)
            fert()

print("Успешно!")
