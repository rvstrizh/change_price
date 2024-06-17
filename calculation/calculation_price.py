from calculation.calculation_bonus import Calculation_Price_With_Bonus
from settings import open_json


class Price_Change:
    def __init__(self, price_list, min_price, max_price, sensitivity=1, step=10):
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
            self.old_my_price = [1, 1, 'Курьером СММ']

        filter_delivery_price_list = [v for k, v in self.price_list.items() if 'Курьером СММ' in v]
        sorted_price_list = sorted(filter_delivery_price_list, key=lambda x: x[0])
        self.price_list = list(filter(lambda x: self.max_price >= x[0] >= self.min_price, sorted_price_list))

    def adjust_prices(self):
        new_price = self.max_price
        # Обходим каждый элемент в списке цен
        for i in range(len(self.price_list) - 1):
            if abs(self.price_list[i + 1][0] - self.price_list[i][0]) > self.sensitivity:
                final_my_price = Calculation_Price_With_Bonus(self.old_my_price, self.price_list[i + 1],
                                                              self.price_list[i + 1][0] - self.step,
                                                              self.min_price).run()
                return final_my_price

        return new_price

    def filter_sensitivity(self):
        try:
            self.preparing_list()
            if len(self.price_list) == 0:  # если нет конкурентов ставим максимальную цену
                return self.max_price

            if self.sensitivity == 1:  # чувствительность =1 прилепляемся к минимальной цене в выставленном диапазоне мин мак
                print(self.old_my_price, self.price_list[0],
                                                              self.price_list[0][0] - self.step,
                                                              self.min_price)
                final_my_price = Calculation_Price_With_Bonus(self.old_my_price, self.price_list[0],
                                                              self.price_list[0][0] - self.step,
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
    price_list = {'М.видео': [34999, 700, 'Другие службы доставки'], 'MegaPixel': [34970, 700, 'Курьером СММ'], 'ХОБОТ (доставка МегаМаркет)': [34990, 3500, 'Курьером СММ'], 'АБСОЛЮТ ТРЕЙД Москва (со склада СберМегаМаркет)': [34990, 4550, 'Курьером СММ'], 'ТЕХНОПАРК (доставка МегаМаркет)': [34990, 700, 'Курьером СММ'], 'Smile': [34980, 700, 'Курьером СММ'], 'WITE': [34980, 700, 'Курьером СММ'], 'Эльдорадо': [34999, 700, 'Курьером СММ'], 'ХОБОТ': [34990, 3500, 'Другие службы доставки'], 'Alt-Dim': [48977, 980, 'Другие службы доставки'], 'Фотосклад Москва': [48766, 976, 'Курьером СММ'], 'Неватека': [49437, 989, 'Курьером СММ'], 'ImperiaTechno SPB': [47485, 950, 'Курьером СММ'], 'ОЛДИ': [42968, 860, 'Курьером СММ'], 'Coolstore': [39430, 789, 'Курьером СММ'], 'Tehhouse': [49932, 999, 'Курьером СММ'], 'Just.ru': [43018, 4733, 'Курьером СММ'], 'OLDI': [42954, 860, 'Другие службы доставки'], 'Фирменный магазин H-2U': [44890, 898, 'Курьером СММ'], 'ИМПЕРИЯ ТЕХНО MSK': [47485, 950, 'Курьером СММ'], 'ИМПЕРИЯ ТЕХНО': [47485, 950, 'Курьером СММ'], 'F5it Новосибирск': [39637, 6343, 'Курьером СММ'], 'GuruTV.ru': [49168, 984, 'Другие службы доставки'], 'TopElectronics': [50057, 1002, 'Другие службы доставки'], 'Topcomputer.ru': [50057, 1002, 'Другие службы доставки'], 'super100k': [51379, 1028, 'Курьером СММ'], 'www.cenam.net': [51970, 1040, 'Другие службы доставки'], 'Just a store': [55980, 1120, 'Курьером СММ'], 'ELEMENTX.Электроника': [55889, 2795, 'Курьером СММ'], 'cenam.net (север)': [51800, 1036, 'Курьером СММ'], 'CENAM.NET ( Юг )': [51800, 1036, 'Курьером СММ'], 'МегаФон | Yota - Официальный магазин': [38489, 770, 'Другие службы доставки']}

    # price_list = {'MegaPixel': [35980, 1, 'Курьером СММ', 1],
    pc = Price_Change(price_list, min_price=30990, max_price=34999, sensitivity=1, step=10).run()
    print('итог', pc)
