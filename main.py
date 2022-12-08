import telebot
import requests
import json
import os
import datetime
import emoji


token = '5361815767:AAGwQlqlJZAXqyJ6R8Igw1fXdaaZkVskOpw'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def helpas(message):
    helps = '''
This bot converts from one valute to enother.
/all - get list.
    '''
    bot.send_message(message.chat.id, helps)


@bot.message_handler(commands=['all'])
def get_all(message):
    bot.send_message(message.chat.id, list_currencies(currencies))


@bot.message_handler(func=lambda x: True)
def bot_convert(message):
    txt = message.text.split()
    if len(txt) != 3:
        bot.reply_to(message, 'wrong format')
    else:
        bot.reply_to(message, str(converter(currencies, txt[0], txt[1], txt[2])))


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

    if currencies:
        currencies = currencies["Valute"]


    return currencies


def list_currencies(currencies):
    flags = {
        'AUD': ":Australia:",
        'AZN': ":Azerbaijan:",
        'GBP': ":United_Kingdom:",
        "AMD": ':Armenia:',
        "BYN": ':Belarus:',
        "BGN": ':Bulgaria:',
        "BRL": ':Brazil:',
        "HUF": ':Hungary:',
        "HKD": ':Hong_Kong_SAR_China:',
        "DKK": ':Denmark:',
        "USD": ':United_States:',
        "EUR": ':Germany:',
        "INR": ':India:',
        "KZT": ':Kazakhstan:',
        "CAD": ':Canada:',
        "KGS": ':Kyrgyzstan:',
        "CNY": ':China:',
        "MDL": ':Moldova:',
        "NOK": ':Norway:',
        "PLN": ':Poland:',
        "RON": ':Romania:',
        "XDR": ':airplane_departure:',
        "SGD": ':Singapore:',
        "TJS": ':Tajikistan:',
        "TRY": ':Turkey:',
        "TMT": ':Turkmenistan:',
        "UZS": ':Uzbekistan:',
        "UAH": ':Ukraine:',
        "CZK": ':Czechia:',
        "SEK": ':Sweden:',
        "CHF": ':Switzerland:',
        "ZAR": ':South_Africa:',
        "KRW": ':South_Korea:',
        "JPY": ':Japan:'
    }
    a = ''
    for i in currencies:
        a += (f'{i} {emoji.emojize(flags[i])} {currencies[i]["Nominal"]} {currencies[i]["Name"]} {currencies[i]["Value"]}  \n')
    return a



def converter(currencies, vfrom, vto, suma):
    vfrom = vfrom.strip().upper()
    vto = vto.strip().upper()
    if vto == 'RUB':
        rezoolt = float(suma) / int(currencies[vfrom]["Nominal"]) * float(currencies[vfrom]["Value"])
    elif vfrom == "RUB":
        rezoolt = float(suma) * int(currencies[vto]["Nominal"]) / float(currencies[vto]["Value"])


    return rezoolt


currencies = get_currencies()
print(list_currencies(currencies))
# print(emoji.emojize('	:Russia:'))

bot.polling(none_stop=True)