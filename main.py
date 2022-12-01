import telebot
import requests
import json
import os
import datetime

def get_currencies():

    currencies = []

    URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

    now = datetime.datetime.now()
    filename = f'{now.year}-{now.month:02d}-{now.day:02d}_currencies.json'

    if not os.path.exists(filename):
        a = requests.get(URL)

        if a.status_code == 200:
            currencies = json.loads(a.text)

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(currencies, f, ensure_ascii=False, indent=4)

            files_to_remove = [file for file in os.listdir() if file.endswith('_currencies.json') and file != filename]
            for i in files_to_remove:
                os.remove(i)

    else:
        with open(filename, 'r', encoding='utf-8') as f:
            currencies = json.load(f)

    return currencies

currencies = get_currencies()

