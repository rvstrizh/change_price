import telebot
import json

min_rating = 4.1
BOT_TOKEN = '7146003508:AAG84UpXM-K7c-5nGv7T1ONnXK5D3aF0OM8'  # рабочий
# BOT_TOKEN = '6727606383:AAECPs31PX2yU9lG7fQV3Qg7j7zPoH1IT-k' # тестовый
bot = telebot.TeleBot(BOT_TOKEN)
category_dict = {
    'Roman': [8, 204, 359, 82, 112, 161, 185, 194, 205, 206, 219, 253, 254, 255, 257, 283, 284, 297, 298, 299, 300, 301,
              302, 305, 319, 322, 323, 326, 327, 333, 339, 344, 347, 348, 349, 350, 351, 358, 360, 364, 366, 367, 368,
              369, 371, 372, 373, 374, 379],
    'Dmitriy': [0, 196, 11, 136, 167, 170, 176, 182, 183, 19, 235, 236, 237, 238, 239, 240, 241, 243, 244, 245, 246, 247, 248,
                251, 252, 285, 286, 287, 289, 290, 291, 293, 294, 303, 304, 306, 307, 308, 309, 310, 311, 317, 318, 320,
                324, 340, 343, 361, 362, 363, 375],
    "Andrey_P": [380, 7, 139, 144, 145, 164, 179, 180, 181, 186, 187, 188, 189, 190, 191, 192, 193, 207, 209, 216, 217, 218,
                 220, 221, 222, 267, 268, 269, 270, 271, 272, 274, 279, 313, 314, 321, 325, 330, 335, 337, 338, 342],
    "Sergey": [127, 202, 203, 259, 334, 346, 357],
    "Andrey_K": [79, 175, 197, 198, 199, 200, 201, 208, 210, 211, 212, 213, 214, 224, 225, 226, 227, 228, 229, 230, 231,
                 232, 233, 249, 273, 275, 276, 280, 281, 282, 332, 356]}
proxy = '193.124.177.248:9515'
login_proxy = '4ren8c'
password_proxy = 'K1W9CM'


def past_site(sku):
    url_site = f'<a href="http://megapolis-mobile.ru/administrator/index.php?page=product.product_form&limitstart=0&keyword=&product_id={sku}&product_parent_id=&option=com_virtuemart">{sku}</a>'
    return url_site


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
