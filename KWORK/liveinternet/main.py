import csv
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

stolb = ['Website link', 'Number of visitors per month', 'Traffic share']
cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

c = 0
number_of_pages = 5

name_1 = f'Statistic_{cur_time}.csv'
with open(f"{name_1}", 'w') as file:
    writer = csv.writer(file)
    writer.writerow(stolb)

urls = open('urls.txt', 'r').read().split("\n")

for item in urls:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(item)
    for i in range(4):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.close()

    for item in soup.find_all(class_="result result-sm clearFix"):
        c += 1
        name = item.find_next(class_="text").find('a').get("href")
        if item.find_next("span") == None:
            percent = '80%'
        else:
            percent = item.find_next("span").text
        peoples = item.find_next(class_="result-num").text.replace(" ", "")
        with open(f"{name_1}", 'a') as file:
            writer = csv.writer(file)
            writer.writerow([f"{name}", f"{peoples}", f"{percent}"])
