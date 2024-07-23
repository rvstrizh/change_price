import telebot
import json
min_rating = 4.1
BOT_TOKEN = '7146003508:AAG84UpXM-K7c-5nGv7T1ONnXK5D3aF0OM8' # рабочий
# BOT_TOKEN = '6727606383:AAECPs31PX2yU9lG7fQV3Qg7j7zPoH1IT-k' # тестовый
bot = telebot.TeleBot(BOT_TOKEN)
category_dict = {'Roman': [194, 219, 299, 300, 323, 206, 257, 204, 319, 359, 372, 358, 298, 322, 326, 360, 379, 298, 364], 'Dmitriy': [167, 297, 251, 320, 11, 170], "Andrey_P": [218, 190, 188, 187, 189, 191, 192], "Sergey": [], "Andrey_K": []}
proxy = '193.124.177.248:9515'
login_proxy = '4ren8c'
password_proxy = 'K1W9CM'


def open_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
        return data


def got_notice(product_id, product_name):
    with open('./not_notice.json', 'r') as f:
        data = json.load(f)
    try:
        if data[product_name]:
            return False
    except KeyError:
        data[product_name] = product_id
        with open('./not_notice.json', 'w') as f:
            json.dump(data, f)
        return True


class CaptchaError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

