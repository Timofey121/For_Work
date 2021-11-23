# -*- coding: utf8 -*-
import datetime
from random import randrange
from time import sleep
from selenium import webdriver
import json
import xlsxwriter
import requests


def main(url_of_group):
    tg = datetime.datetime.now()
    prices = []
    name_shop = []
    s = []
    data = []
    if url_of_group == "https://catalog.onliner.by/office_chair":
        ber = "office_chair"
        rt = "Офисные кресла и стулья"
    else:
        if url_of_group == "https://catalog.onliner.by/table":
            ber = "table"
            rt = "Письменные и компьютерные столы"
        else:
            if url_of_group == "https://catalog.onliner.by/chair":
                ber = "chair"
                rt = "Стулья для кухни и бара"
            else:
                if url_of_group == "https://catalog.onliner.by/kidsdesk":
                    ber = "kidsdesk"
                    rt = "Детские парты, столы, стулья"
                else:
                    if url_of_group == "https://catalog.onliner.by/gardenfurniture":
                        ber = "gardenfurniture"
                        rt = "Садовая мебель"
                    else:
                        if url_of_group == "https://catalog.onliner.by/divan":
                            ber = "divan"
                            rt = "Диваны"
                        else:
                            ber = "interior_chair"
                            rt = "Кресла"
    w = 0
    dr = ""
    hj = ""
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)
    for i in range(1, 5):
        req = requests.get(url=f"https://catalog.onliner.by/sdapi/catalog.api/search/{ber}?group=1&page={i}")
        jso = json.loads(req.text)
        for j in range(0, 30):
            from_selenium = jso['products'][j]['html_url']
            name = jso['products'][j]['full_name']
            html = jso['products'][j]['html_url'].split('/')[-1]
            r = requests.get(
                url=f"https://catalog.onliner.by/sdapi/shop.api/products/{html}/positions?town=all")
            json_data = json.loads(r.text)
            quantity = json_data["positions_count_by_town"][json_data["towns"][0]['key']]
            driver.get(from_selenium + "/prices")
            # print(quantity)
            sleep(1.7)
            a = driver.find_elements_by_class_name("offers-list__description_nowrap")
            for o in a:
                # print(o.text)
                if len(o.text.split()) == 4 and o.text.split()[-1] == '—':
                    s.append(o.text)
                    print(o.text)

            # print(s)
            for k in range(0, len(s)):
                if not json_data["shops"][str(json_data["positions"]["primary"][k]["shop_id"])]["title"] == "KingStyle":
                    prices.append(json_data['positions']['primary'][k]['position_price']['amount'])
                    name_shop.append(
                        json_data["shops"][str(json_data["positions"]["primary"][k]["shop_id"])]["title"])

                else:
                    dr = json_data['positions']['primary'][k]['position_price']['amount']
                    hj = s[k]
                    # print(dr)
                    # print(hj)
                    w = 1
                    if len(s) < 2:
                        s = []
                    else:
                        del s[k]
            # print(s)

            if w == 1:
                na = "Есть в магазине KingStyle"
            else:
                na = "Нет в магазине KingStyle"
            # print(quantity)
            # print(s)
            if len(s) > 0:
                if len(s) == 1:
                    item = {
                        'name': name,
                        'price': ''.join(prices),
                        'delivery': "Доставка " + ' '.join(s),
                        'price_King': dr,
                        'delivery_King': "Доставка " + hj,
                        'name_shop': ', '.join(name_shop),
                        'url': from_selenium + "/prices",
                        'nal': na
                    }

                else:
                    if w == 1:
                        item = {
                            'name': name,
                            'price': min(prices),
                            'delivery': "Доставка " + str(s[prices.index(min(prices))]),
                            'price_King': dr,
                            'delivery_King': "Доставка " + hj,
                            'name_shop': ', '.join(name_shop),
                            'url': from_selenium + "/prices",
                            'nal': na
                        }
                    else:
                        item = {
                            'name': name,
                            'price': min(prices),
                            'delivery': "Доставка " + str(s[prices.index(min(prices))]),
                            'price_King': " ",
                            'delivery_King': " ",
                            'name_shop': ', '.join(name_shop),
                            'url': from_selenium + "/prices",
                            'nal': na
                        }
            else:
                if name_shop:
                    if w == 1:
                        item = {
                            'name': name,
                            'price': ''.join(prices),
                            'delivery': "Пока нет доставки по адресу и в пункты выдачи",
                            'price_King': dr,
                            'delivery_King': "Доставка " + hj,
                            'name_shop': ', '.join(name_shop),
                            'url': from_selenium + "/prices",
                            'nal': na
                        }
                    else:
                        item = {
                            'name': name,
                            'price': ''.join(prices),
                            'delivery': "Пока нет доставки по адресу и в пункты выдачи",
                            'price_King': dr,
                            'delivery_King': hj,
                            'name_shop': ', '.join(name_shop),
                            'url': from_selenium + "/prices",
                            'nal': na
                        }

                else:
                    item = {
                        'name': name,
                        'price': "Такого товара нет, кроме как в KingStyle",
                        'delivery': "Такого товара нет, кроме как в KingStyle",
                        'price_King': dr,
                        'delivery_King': "Доставка " + hj,
                        'name_shop': ', '.join(name_shop),
                        'url': from_selenium + "/prices",
                        'nal': na
                    }
            data.append(item)
            prices = []
            s = []
            w = 0
            name_shop = []
            dr = ''
            hj = ''

            with xlsxwriter.Workbook(f"{rt}.xlsx") as workbook:
                ws = workbook.add_worksheet()
                bold = workbook.add_format({'bold': True})

                headers = ['Название товара', 'Цена', "Сроки доставки", "Цена KingStyle", "Сроки доставки KingStyle",
                           "Магазин срока доставки", "Ссылка", "Наличие"]
                for col, h in enumerate(headers):
                    ws.write_string(0, col, h, cell_format=bold)
                for row, item in enumerate(data, start=1):
                    ws.write_string(row, 0, item["name"])
                    ws.write_string(row, 1, item["price"])
                    ws.write_string(row, 2, item['delivery'])
                    ws.write_string(row, 3, item["price_King"])
                    ws.write_string(row, 4, item["delivery_King"])
                    ws.write_string(row, 5, item['name_shop'])
                    ws.write_string(row, 6, item["url"])
                    ws.write_string(row, 7, item['nal'])

        print(f"Обработана {i}/{4}")
    print(datetime.datetime.now() - tg)


if __name__ == "__main__":
    main("https://catalog.onliner.by/kidsdesk")
