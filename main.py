import telebot
import requests

#TODO: получить данные о валютах
URL = 'https://www.cbr-xml-daily.ru/daily_json.js'
a = requests.get(URL)
if a.status_code == 200:
    b = open(a)
