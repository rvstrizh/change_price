from calculation_bonus import Calculation_Price_With_Bonus


class Price_Change:
    def __init__(self, price_list, min_price, max_price, sensitivity=0, step=10):
        self.price_list = price_list
        self.min_price = min_price
        self.max_price = max_price
        self.sensitivity = sensitivity
        self.step = step

    def preparing_list(self):
        try:
            # сделать если мы одни торгуем этим товаром
            self.old_my_price = self.price_list['MegaPixel']  # 'MegaPixel': [67990, 642, 'Доставка по клику, ', 1]
            del self.price_list['MegaPixel']
        except KeyError:
            self.old_my_price = [100, 1, 'Курьером СММ']

        filter_delivery_price_list = [v for k, v in self.price_list.items() if 'Курьером СММ' in v]
        sorted_price_list = {item[0]: item for item in sorted(filter_delivery_price_list, key=lambda x: (x[0], x[1]))}
        sorted_price_list = list(sorted_price_list.values())
        self.price_list = list(filter(lambda x: self.max_price >= x[0] >= self.min_price, sorted_price_list))

    def comparison_neighboring_price(self):
        percent_my_bonus = int(self.old_my_price[1] * 100 / self.old_my_price[0])
        percent_first_element = int(self.price_list[0][1] * 100 / self.price_list[0][0])
        percent_second_element = int(self.price_list[1][1] * 100 / self.price_list[1][0])
        if percent_first_element < percent_my_bonus <= percent_second_element:
            return self.price_list[1]
        else:
            return self.price_list[0]

    def adjust_prices(self):
        new_price = self.price_list[0][0] - self.step
        try:
            # Обходим каждый элемент в списке цен
            for i in range(2):
                if abs(self.price_list[i + 1][0] - self.price_list[i][0]) > self.sensitivity:
                    final_my_price = Calculation_Price_With_Bonus(self.old_my_price, self.price_list[i + 1],
                                                                  self.price_list[i + 1][0] - self.step,
                                                                  self.min_price).run()
                    return final_my_price
            return new_price
        except IndexError:
            return new_price

    def filter_sensitivity(self):
        try:
            self.preparing_list()
            if len(self.price_list) == 0:  # если нет конкурентов ставим максимальную цену
                return self.max_price

            if not self.sensitivity:  # чувствительность =0 или не заполнено прилепляемся к минимальной цене в выставленном диапазоне мин мак
                # [20923, 1674, 'Курьером СММ'] [20890, 418, 'Курьером СММ'] 20390 18990
                if len(self.price_list) == 1:
                    list_property = self.price_list[0]
                else:
                    list_property = self.comparison_neighboring_price()
                print(self.old_my_price, list_property,
                                                              list_property[0] - self.step,
                                                              self.min_price)
                final_my_price = Calculation_Price_With_Bonus(self.old_my_price, list_property,
                                                              list_property[0] - self.step,
                                                              self.min_price).run()
                return final_my_price
            else:
                return self.adjust_prices()
        except KeyError:
            # дописать код что бы было уведомление в телегу что товар вымещен, но бот его не видит
            pass

    def run(self):
        return self.filter_sensitivity()


if __name__ == '__main__':
    price_list = {'SIBDROID (МОСКВА)': [33590, 0, 'Другие службы доставки'],
                   'Sold-Out (RUS)': [34788, 1740, 'Курьером СММ'],
                   'MegaPixel': [34990, 700, 'Курьером СММ'],
                   'Guru Mobile': [35120, 703, 'Курьером СММ'],
                   'СОТОВИКmobile': [34700, 694, 'Другие службы доставки'],
                   'Lite Mobile FBS': [37430, 749, 'Курьером СММ']
}

    # price_list = {'MegaPixel': [35980, 1, 'Курьером СММ', 1],
    pc = Price_Change(price_list, min_price=34590, max_price=36990, sensitivity=1000, step=10).run()
    print('итог', pc)
