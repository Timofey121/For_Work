import datetime
import time

import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

file = open('1.txt').readlines()  # если у Вас ссылки будут лежать в файле с другим названием, тут нужно будет поменять
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for item in file:
    try:
        connection = mysql.connector.connect(
            host='195.93.173.230',
            port=3306,
            user='admin_vi_new',
            passwd='FbC3JN9xMlA1C7tl',
            db='admin_vi_new'
        )
        driver.get(item.replace("\n", ""))
        time.sleep(0.2)

        soup = BeautifulSoup(driver.page_source, "lxml")
        article_number = soup.find(class_="product-code").find(class_="value").text.strip()
        try:
            quantity = soup.find(class_="text -black").text.strip().replace("Есть на складе: ", "").replace(" шт.",
                                                                                                            "").strip()
            amount = soup.find(class_="current-price").text.strip()
        except Exception as ex:
            try:
                quantity = "Нет товаров в наличии! Можно только " + soup.find(
                    class_="add-to-card button -primary -outlined -x-large -full-width").text.strip().lower()
                amount = soup.find(class_="current-price -grey").text.strip()
            except Exception as ex:
                quantity = "Нет информации о количестве!"
                try:
                    amount = soup.find(class_="current-price").text.strip()
                except:
                    amount = "Цена не указана"

        cur = connection.cursor()
        cur.execute(f"SELECT * FROM vseinstrumenti WHERE article_number='{article_number}'")
        rows = cur.fetchall()
        if len(rows) != 0:
            cur.execute(
                f"UPDATE vseinstrumenti SET amount='{amount}', quantity='{quantity}' WHERE article_number="
                f"'{article_number}'")
        else:
            cur.execute(
                f"INSERT INTO vseinstrumenti (article_number, amount, quantity) VALUES ('{article_number}', '{amount}',"
                f" '{quantity}')")
        connection.commit()
        connection.close()
    except Exception as ex:
        pass

