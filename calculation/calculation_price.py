from itertools import chain
from bs4 import BeautifulSoup
import re

from calculation.calculation_bonus import Calculation_Price_With_Bonus


class Price_Change:
    def __init__(self, price_list, min_price=34000, max_price=75000, sensitivity=1500, step=10):
        self.price_list = price_list
        self.min_price = min_price
        self.max_price = max_price
        self.sensitivity = sensitivity
        self.step = step

    def run(self):
        price_list = {k: v for k, v in self.price_list.items() if 'Курьером СММ' in v}
        all_prices = dict(sorted(price_list.items(), key=lambda x: x[1][0]))
        try:
            old_my_price = all_prices['MegaPixel']  # 'MegaPixel': [67990, 642, 'Доставка по клику, ', 1]
            del all_prices['MegaPixel']
        except:
            old_my_price = [1, 1, 'Доставка по клику, ', 1]
        # prev_key - название магазина, prev_value - список [цена, кешбек, способ доставки]
        name_shop, list_property = next(iter(all_prices.items()))
        # сравниваем первый со вторым второй с третьим и тд
        print(list_property)
        for key, value in all_prices.items():
            print(value[0], list_property[0])
            difference = value[0] - list_property[0]
            my_price = list_property[0] - self.step
            print('my_price', my_price)
            # 1510 > 1520
            if difference > self.sensitivity:
                print(f"Разница между {name_shop} и {key} ({list_property} и {value}): {difference}")

                if my_price >= self.min_price - 90:  # возможно убрать тк эту разницу можно учитывать в шаге цены
                    final_my_price = Calculation_Price_With_Bonus(old_my_price, list_property, my_price,
                                                                  self.min_price).run()
                    # теперь нужно учитывать размер кешбека если он большой у меня
                    return final_my_price
            elif self.sensitivity == 1:
                final_my_price = Calculation_Price_With_Bonus(old_my_price, list_property, my_price,
                                                              self.min_price).run()
                # теперь нужно учитывать размер кешбека если он большой у меня
                return final_my_price

            name_shop, list_property = key, value


#######
# all_prices = dict(sorted(self.price_list.items(), key=lambda x: x[1][0]))
# my_price = all_prices['MegaPixel']  # 'MegaPixel': [67990, 642, 'Доставка по клику, ', 1]
# del all_prices['MegaPixel']
# shops = [s for s, _ in all_prices.items()]  # список магазинов
# counter = 0
# for shop in shops:
#     counter += 1
#     if 'Забрать' not in all_prices[shop][2]:
#         if all_prices[shop][0] - my_price[0] != 10:
#             return all_prices[shop][0] - 10
######

# Класс должен дать добро сохраняем ссылку для закупа или нет
# Первая проверка по цене без кешбека на списание
# Вторая проверка с кешбеком на начисление
class Search_Prices_For_Purchase:
    def __init__(self, price_list):
        self.price_list = price_list
        self.flag = False

    def search_for_accrual(self):  # буду возвращать слово 'Накопление'
        price_cash = [price[0] for _, price in self.price_list.items()]
        best_price = min(price_cash)
        price_cash.remove(best_price)
        # может быть один товар и когда я его удаляю уже мин прайс нельзя найти
        # например Samsung SM-X806 Galaxy Tab S8+ LTE 128Gb Black (RU)
        try:
            if best_price + best_price * 0.20 < min(price_cash):
                self.flag = [best_price, 'Накопление']
        except ValueError:
            pass

    def search_for_write_off(self):  # буду возвращать слово 'Списание'
        price_cash = [[price[0], price[1]] for _, price in self.price_list.items()]
        price_cash_ball = sorted(price_cash, key=lambda x: x[1])
        min_price = price_cash_ball[0][0]
        price_cash_ball = list(map(lambda x: x[0] - x[1], price_cash_ball))
        if min_price + min_price * 0.35 < min(price_cash_ball):
            self.flag = [best_price, 'Списание']

    def run(self):
        if len(self.price_list) > 1:
            self.search_for_accrual()
            self.search_for_write_off()
            return self.flag
        else:
            return False


if __name__ == '__main__':
    price_list = {'Мегамаркет Москва КГТ': [35990, 1, 'Курьером СММ'],
                  'Фирменный магазин POLARIS Вешки (со склада МегаМаркет)': [37500, 15000, 'Курьером СММ'],
                  'Фирменный магазин POLARIS СПб (со склада МегаМаркет)': [37600, 15000, 'Курьером СММ'],
                  'Фирменный магазин POLARIS ЕКБ (со склада МегаМаркет)': [37900, 15000, 'Курьером СММ'],
                  'ОГО! Онлайн-гипермаркет (DSM)': [60409, 605, 'Другие службы доставки'],
                  'Техника в быту': [73917, 740, 'Курьером СММ'],
                  'ИП Романова Татьяна Павловна': [82721, 828, 'Курьером СММ'],
                  'RKStore': [113220, 1133, 'Курьером СММ'],
                  'Магазин Polaris': [49990, 11499, 'Другие службы доставки'],
                  'ОГО! Онлайн-гипермаркет (С&C)': [60409, 605, 'Другие службы доставки']}
    # if 'MegaPixel' in price_list:
    #     best_price = Price_Change(price_list).run()
    #     print(best_price)
    # price_list = {'Ситилинк Москва Доставка': [47420, 6641, 'Доставка курьером продавца, ']}
    pc = Price_Change(price_list).run()
    print('итог', pc)
