import json
import time
import schedule
from datetime import datetime
import xlsxwriter

from connect_sql import read_sql
from driver import installation
from parse import Parse_Page
from calculation.calculation_purchase import Search_Prices_For_Purchase
from calculation.calculation_price import Price_Change
from settings import CaptchaError, category_dict, bot, open_json


def create_file():
    names = ['Roman', 'Dmitriy', 'Andrey_P']
    for name in names:
        name_file = f'./offers_price/{name}.xlsx'
        workbook = xlsxwriter.Workbook(name_file)
        workbook.add_worksheet()
        workbook.close()


def write_json(price):
    with open('bd_sql.json', 'w') as f:
        json.dump(price, f, indent=4)


schedule.every().day.at("23:50").do(create_file)


class Main:
    def __init__(self):
        self.stock = None
        self.product_name = None
        self.product_id = None
        self.category = None
        self.url_smm = None
        self.old_my_price = None
        self.min_price = None
        self.max_price = None
        self.sensitivity = None
        self.step = None
        # self.user_agent = installation()
        self.user_agent ='Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'

    def parse(self, url_smm):
        while True:
            try:
                price_list = Parse_Page(url_smm, self.user_agent).show_shop()
                return price_list
            except CaptchaError:
                self.user_agent = installation()

    def new_price(self):
        price_list = self.parse(self.url_smm)
        ######
        print(price_list)
        #####
        if self.stock:
            if 'MegaPixel' not in price_list:
                # поставить сигнал боту что силениум не нашел наш магазин, хотя товар в наличии
                bot.send_message(1315757744, f'Не нашел наш магазин,на товар sku {self.product_id} хотя наличие в админке проставлено убедись точно вот ссылка:\n{self.url_smm}')
                Search_Prices_For_Purchase(price_list, self.category, self.product_name, self.url_smm, self.old_my_price).run()
            return Price_Change(price_list, self.min_price, self.max_price, self.sensitivity, self.step).run()
        else:
            # прописать с товаром которого нет в наличии, но нам нужно посмотреть карточку на выгодный кешбек и просто на низкую цену
            pass

    def run(self):
        for i in range(1):
        # while True:
            current_hour = datetime.now().hour
            if 12 <= current_hour < 23:
                json_file = open_json('bd_sql.json')
                if json_file:
                    self.product_name = json_file[0]['product_sku']
                    self.product_id = json_file[0]['product_id']
                    self.category = json_file[0]['category']
                    self.url_smm = json_file[0]['url_SMM']
                    self.old_my_price = json_file[0]['product_order_levels']
                    self.min_price = json_file[0]['min_price_smm']
                    self.max_price = json_file[0]['max_price_SMM']
                    self.sensitivity = json_file[0]['sensitivity']
                    self.step = json_file[0]['step']
                    self.stock = json_file[0]['product_in_stock']

                    if all([self.url_smm, self.min_price, self.max_price]):
                        self.old_my_price = int(self.old_my_price.replace("0,", ""))
                        new_price = self.new_price()
                        # write_sql(new_price, product_id) изменение цены в sql
                        # временное дополнение что бы не менять автоматом цену
                        if self.old_my_price != new_price:
                            bot.send_message(1315757744, f'Поменяй цену sku {self.product_id} на {new_price} вот тебе ссылка на мегамаркет {self.url_smm}')
                        write_json(json_file[1:])
                    else:
                        write_json(json_file[1:])
                        manager = [man for man, cat in category_dict.items() if self.category in cat]
                        m = [k for k, v in open_json('data.json').items() if v == manager[0]]
                        bot.send_message(m[0], f'В товаре {self.product_name} sku {self.product_id}\nurl_smm = {self.url_smm}\nmin_price = {self.min_price}\nmax_price = {self.max_price}')
                else:
                    read_sql()

            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    # print(open_json('data.json'))
    Main().run()
