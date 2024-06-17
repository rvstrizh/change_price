import telebot
import json
min_rating = 4.1
BOT_TOKEN = '7146003508:AAG84UpXM-K7c-5nGv7T1ONnXK5D3aF0OM8'
bot = telebot.TeleBot(BOT_TOKEN)
category_dict = {'Roman': [194, 219, 299, 300, 323, 206, 257, 204, 319], 'Dmitriy': []}

proxy = '193.124.177.248:9515'
login_proxy = '4ren8c'
password_proxy = 'K1W9CM'


def open_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
        return data


class CaptchaError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

