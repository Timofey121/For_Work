import datetime
import os

import mysql.connector
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

name_file = '1.txt'

file = open(name_file).readlines()
useragent = UserAgent()
headers = {
    "User-Agent": str(useragent.random)
}
print(headers)
connection = mysql.connector.connect(
    host='195.93.173.230',
    port=3306,
    user='admin_vi_new',
    passwd='FbC3JN9xMlA1C7tl',
    db='admin_vi_new'
)
cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
for i in range(min(4500, len(file))):
    item = file[i]
    url = item.replace("\n", "")

    try:
        src = requests.get(item.replace("\n", ""), headers=headers)
        soup = BeautifulSoup(src.text, "lxml")
        if soup.find(class_="page-not-found") is None:
            k = 0
            while k != 1:
                try:
                    article_number = soup.find(class_="product-code").find(class_="value").text.strip()
                    k = 1
                except Exception as ex:
                    useragent = UserAgent()
                    headers = {
                        "User-Agent": str(useragent.random)
                    }
                    print(ex, headers)
                    src = requests.get(item.replace("\n", ""), headers=headers)
                    soup = BeautifulSoup(src.text, "lxml")
            try:
                quantity = soup.find(class_="text -black").text.strip()
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
            print(f'С ссылкой {url} все хорошо')
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
        else:
            print(f'Некоректная ссылка {url}')
            with open(f"inactive_links_{cur_time}.txt", "a") as file:
                file.write(item)
    except Exception as ex:
        print(f"У ссылки {url} ошибка {ex}")
        useragent = UserAgent()
        headers = {
            "User-Agent": str(useragent.random)
        }

file_1 = []

for i in range(min(4500, len(file))):
    file_1.append(file[i])

for i in range(min(4500, len(file))):
    del file[0]

for i in range(min(4500, len(file_1))):
    file.append(file_1[i])

os.remove(name_file)

with open(name_file, 'w') as f:
    for item1 in file:
        f.write(item1)
