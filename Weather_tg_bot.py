import telebot
import pymorphy2
from selenium import webdriver
from time import sleep
from tg import *
from selenium.webdriver.common.keys import Keys

bot = telebot.TeleBot()

joinedFile = open('', 'r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()


@bot.message_handler(commands=['start'])
def startJoin(message):
    bot.send_message(message.chat.id, "Привет, это бот, создан для погоды! Напиши '/' и узнай, что может этот бот!")
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open('C:/Users/User/OneDrive/Desktop/for_python.txt', 'a')
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(message.chat.id)


@bot.message_handler(commands=['special'])
def mess(message):
    for user in joinedUsers:
        bot.send_message(user, message.text[message.text.find(' '):])


@bot.message_handler(commands=['weather_now'])
def weather_now(message):
    msg = bot.send_message(message.chat.id, "Введите город, погоду которого вы хотите найти!")
    bot.register_next_step_handler(msg, search)


def search(msg):
    bot.send_message(msg.chat.id, "Начинаю поиск, подождите немного!")
    sleep(2)
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)

    driver.get('https://pogoda.mail.ru/prognoz/sankt_peterburg/')

    search = driver.find_element_by_xpath(
        '//*[@id="portal-menu__toolbar"]/div/div/div[2]/div/span/span[2]/span/span/form/span[1]/span[1]/input')
    search.send_keys(msg.text)
    search.send_keys(Keys.ENTER)

    weather = driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[1]/a/div[1]/div[1]')
    morse = pymorphy2.MorphAnalyzer()
    a = morse.parse(msg.text)[0]
    bot.send_message(msg.chat.id, 'Сейчас в ' + str(a.inflect({'loct'}).word.capitalize()) + ' '
                     + weather.text + ' градусов!')


@bot.message_handler(commands=['weather_in_the_evening'])
def weather_in_the_evening(message):
    msg = bot.send_message(message.chat.id, "Введите город, погоду которого вы хотите найти!")
    bot.register_next_step_handler(msg, f)


def f(msg):
    bot.send_message(msg.chat.id, "Начинаю поиск, подождите немного!")
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)

    driver.get('https://pogoda.mail.ru/prognoz/sankt_peterburg/')

    search = driver.find_element_by_xpath(
        '//*[@id="portal-menu__toolbar"]/div/div/div[2]/div/span/span[2]/span/span/form/span[1]/span[1]/input')
    search.send_keys(msg.text)
    search.send_keys(Keys.ENTER)

    weather = driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/a/div[1]/div[3]')
    morse = pymorphy2.MorphAnalyzer()
    a = morse.parse(msg.text)[0]
    bot.send_message(msg.chat.id, 'Вечером в ' + str(a.inflect({'loct'}).word.capitalize()) + ' '
                     + weather.text + ' градусов!')


@bot.message_handler(commands=['weather_at_nigth'])
def weather_at_night(message):
    msg = bot.send_message(message.chat.id, "Введите город, погоду которого вы хотите найти!")
    bot.register_next_step_handler(msg, d)


def d(msg):
    bot.send_message(msg.chat.id, "Начинаю поиск, подождите немного!")
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)

    driver.get('https://pogoda.mail.ru/prognoz/sankt_peterburg/')

    search = driver.find_element_by_xpath(
        '//*[@id="portal-menu__toolbar"]/div/div/div[2]/div/span/span[2]/span/span/form/span[1]/span[1]/input')
    search.send_keys(msg.text)
    search.send_keys(Keys.ENTER)

    weather = driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/a/div[2]/div[3]')
    morse = pymorphy2.MorphAnalyzer()
    a = morse.parse(msg.text)[0]
    bot.send_message(msg.chat.id, 'Ночью в ' + str(a.inflect({'loct'}).word.capitalize()) + ' '
                     + weather.text + ' градусов!')


@bot.message_handler(commands=['weather_tomorrow'])
def weather_tomorrow(message):
    msg = bot.send_message(message.chat.id, "Введите город, погоду которого вы хотите найти!")
    bot.register_next_step_handler(msg, e)


def e(msg):
    bot.send_message(msg.chat.id, "Начинаю поиск, подождите немного!")
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)

    driver.get('https://pogoda.mail.ru/prognoz/sankt_peterburg/')

    search = driver.find_element_by_xpath(
        '//*[@id="portal-menu__toolbar"]/div/div/div[2]/div/span/span[2]/span/span/form/span[1]/span[1]/input')
    search.send_keys(msg.text)
    search.send_keys(Keys.ENTER)

    weather = driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/a/div[3]')
    morse = pymorphy2.MorphAnalyzer()
    a = morse.parse(msg.text)[0]
    bot.send_message(msg.chat.id, 'Завтра в ' + str(a.inflect({'loct'}).word.capitalize()) + ' '
                     + weather.text + ' градусов!')


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, "Такой команды нет! "
                                      "Если хочешь узнать погоду,"
                                      " напиши weather_now or weather_tomorrow"
                                      " or weather_at_night or weather_at_the_evening!"
                                      " Или просто напиши '/' и он выдаст тебе список команд, которые умеет этот бот!")


bot.polling()
