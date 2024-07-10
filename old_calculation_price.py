from calculation_bonus import Calculation_Price_With_Bonus


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
        print(self.price_list)

    def adjust_prices(self):
        new_price = self.max_price
        # Обходим каждый элемент в списке цен
        for i in range(len(self.price_list)):
            # print('prices[i]', prices[i])
            # Если не первый элемент, сравниваем с предыдущим
            print(self.price_list[i][0], self.price_list[i - 1][0])
            if i > 0:
                if abs(self.price_list[i][0] - self.price_list[i - 1][0]) > self.sensitivity:
                    self.price_list[i][0] = self.price_list[i - 1][0] - self.step
                    if self.price_list[i][0] >= self.min_price:
                        print(1, self.old_my_price, self.price_list[i - 1],
                                                                      self.price_list[i][0],
                                                                      self.min_price)
                        final_my_price = Calculation_Price_With_Bonus(self.old_my_price, self.price_list[i - 1],
                                                                      self.price_list[i][0],
                                                                      self.min_price).run()
                        return final_my_price
            # Если не последний элемент, сравниваем со следующим
            if i < len(self.price_list) - 1:
                if abs(self.price_list[i][0] - self.price_list[i + 1][0]) > self.sensitivity:
                    self.price_list[i][0] = self.price_list[i + 1][0] - self.step
                    if self.price_list[i][0] >= self.min_price:
                        print(2, self.old_my_price, self.price_list[i - 1],
                              self.price_list[i][0],
                              self.min_price)
                        final_my_price = Calculation_Price_With_Bonus(self.old_my_price, self.price_list[i - 1],
                                                                      self.price_list[i][0],
                                                                      self.min_price).run()
                        return final_my_price
            # print('new_price', new_price)
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


if __name__ == '__main__':
    price_list = {'MegaPixel': [41590, 832, 'Курьером СММ'], 'HOLODILNIK.RU (Север)': [43699, 6555, 'Курьером СММ'], 'Технопарк - СберМаркет': [39990, 800, 'Другие службы доставки'], 'Lite Mobile FBS': [43660, 874, 'Курьером СММ'], 'ХОБОТ (доставка МегаМаркет)': [39990, 4000, 'Курьером СММ'], 'АБСОЛЮТ ТРЕЙД Москва (со склада СберМегаМаркет)': [39990, 5200, 'Курьером СММ'], 'Alt-Dim': [51970, 1040, 'Другие службы доставки'], 'XCOM-SHOP': [40194, 804, 'Курьером СММ'], 'ХОБОТ': [39990, 4000, 'Другие службы доставки'], 'Ultra-Media.ru': [41700, 4587, 'Курьером СММ'], 'Пантелеком': [41790, 4598, 'Курьером СММ'], 'GSM Butik': [43660, 4803, 'Курьером СММ'], 'HOLODILNIK.RU': [43199, 6480, 'Другие службы доставки'], 'Экспресс-доставка техники': [43940, 879, 'Другие службы доставки'], 'Topcomputer.ru': [49619, 993, 'Другие службы доставки'], 'TopElectronics': [49619, 993, 'Другие службы доставки'], 'Tehhouse': [60106, 1203, 'Курьером СММ'], 'АЛЕВИТ': [47833, 957, 'Курьером СММ'], 'Фотосклад Санкт-Петербург': [50936, 1019, 'Курьером СММ'], 'Официальный магазин BrandBooster Санкт-Петербург': [50936, 1019, 'Курьером СММ'], 'Официальный магазин BrandBooster Москва': [50936, 1019, 'Курьером СММ'], 'Фотосклад Москва': [50936, 1019, 'Курьером СММ'], 'Бонатека BP': [48730, 975, 'Курьером СММ'], 'Неватека (FBS)': [51571, 1032, 'Курьером СММ'], 'Gogol': [52216, 1045, 'Курьером СММ'], 'Реал связь': [43000, 4730, 'Курьером СММ'], 'NiceOneElectronics': [54100, 1082, 'Курьером СММ'], 'i-Stock.store': [46199, 924, 'Курьером СММ'], 'halloha.ru': [46199, 924, 'Курьером СММ'], 'смартфон74.рф': [46199, 924, 'Курьером СММ'], 'Just a store': [66480, 1330, 'Курьером СММ'], 'MULTISTORE.Shop': [73409, 3671, 'Курьером СММ'], 'Pleer.Ru (самовывоз из магазина)': [44873, 898, 'Другие службы доставки'], 'МегаФон | Yota - Официальный магазин': [46189, 924, 'Другие службы доставки']}

    # price_list = {'MegaPixel': [35980, 1, 'Курьером СММ', 1],
    pc = Price_Change(price_list, min_price=39970, max_price=41820, sensitivity=800, step=10).run()
    print('итог', pc)
