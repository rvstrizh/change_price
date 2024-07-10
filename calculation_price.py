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
            self.old_my_price = [1, 1, 'Курьером СММ']

        filter_delivery_price_list = [v for k, v in self.price_list.items() if 'Курьером СММ' in v]
        sorted_price_list = sorted(filter_delivery_price_list, key=lambda x: x[0])
        self.price_list = list(filter(lambda x: self.max_price >= x[0] >= self.min_price, sorted_price_list))
        print(self.price_list)

    def adjust_prices(self):
        new_price = self.price_list[0][0] - self.step
        # Обходим каждый элемент в списке цен
        for i in range(2):
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

            if self.sensitivity == 0:  # чувствительность =0 прилепляемся к минимальной цене в выставленном диапазоне мин мак
                # [20923, 1674, 'Курьером СММ'] [20890, 418, 'Курьером СММ'] 20390 18990
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
    price_list = {'Resanta (Техномир)': [22151, 8198, 'Курьером СММ'], 'Ситилинк Москва Доставка': [20890, 418, 'Другие службы доставки'], 'Группа компаний Ресанта': [22152, 8198, 'Курьером СММ'], 'Официальный магазин РЕСАНТА | HUTER | ВИХРЬ': [21929, 8115, 'Курьером СММ'], 'Alt-Dim': [25770, 516, 'Другие службы доставки'], 'RESANTA_GLOBAL': [20890, 418, 'Курьером СММ'], 'GARDEN-MARKET': [20890, 3970, 'Курьером СММ'], 'Официальный производитель РЕСАНТА, HUTER, ВИХРЬ': [20890, 418, 'Курьером СММ'], 'Техника для профессионалов': [20890, 209, 'Курьером СММ'], 'MEGABOLT': [20890, 418, 'Курьером СММ'], 'ИНСТРУМЕНТКЛУБ': [20890, 3761, 'Курьером СММ'], 'UTAKE': [20890, 1045, 'Курьером СММ'], 'MegaPixel': [20923, 1674, 'Курьером СММ'], 'БВ Онлайн': [21774, 436, 'Курьером СММ'], 'HOLODILNIK.RU (Юг)': [21999, 2640, 'Курьером СММ'], 'БВ Москва': [21200, 424, 'Другие службы доставки'], 'HOLODILNIK.RU(БСТ)': [21499, 645, 'Другие службы доставки'], 'HOLODILNIK.RU': [21499, 645, 'Другие службы доставки'], 'Resanta_official': [22470, 8316, 'Курьером СММ'], 'СтройСам': [22560, 452, 'Курьером СММ'], 'super100k': [22937, 459, 'Курьером СММ'], 'ИМПЕРИЯ ТЕХНО (ДСМ)': [22380, 448, 'Другие службы доставки'], 'ООО «ЭЛЬТ» (DBS)': [22623, 453, 'Другие службы доставки'], 'ИМПЕРИЯ ТЕХНО MSK': [23580, 472, 'Курьером СММ'], 'ImperiaTechno SPB': [23580, 472, 'Курьером СММ'], 'ИМПЕРИЯ ТЕХНО': [23580, 472, 'Курьером СММ'], 'ATmarket': [24064, 482, 'Курьером СММ'], 'embeq.store': [23240, 465, 'Другие службы доставки'], 'Tehhouse': [24460, 490, 'Курьером СММ'], 'Original Store РЕСАНТА | HUTER | ВИХРЬ': [24576, 9095, 'Курьером СММ'], 'AVTO-1': [23850, 477, 'Другие службы доставки'], 'Кузьма онлайн+': [24859, 4227, 'Курьером СММ'], 'КузьмаМск': [24859, 4227, 'Курьером СММ'], 'MEGA': [24000, 480, 'Другие службы доставки'], 'ЛИНИЯ': [24000, 480, 'Другие службы доставки'], 'ELEMENTX.Инструменты': [27199, 1360, 'Курьером СММ'], 'Topcomputer.ru': [25509, 511, 'Другие службы доставки'], 'TopElectronics': [25509, 511, 'Другие службы доставки'], 'Mnogo.online': [31590, 632, 'Другие службы доставки'], 'Хозяин 43': [20890, 418, 'Курьером СММ'], 'ГК Ресанта (Краснодар)': [22140, 8193, 'Курьером СММ'], 'ООО ТД "Техстроймаркет"': [21880, 438, 'Курьером СММ'], 'ГК Ресанта (Ставрополь)': [22140, 8193, 'Курьером СММ'], 'ГК Ресанта (Сочи)': [22140, 8193, 'Курьером СММ'], 'ГК Ресанта (Центр)': [22574, 8353, 'Курьером СММ'], 'уДачный Фермер FBS': [23801, 477, 'Курьером СММ'], 'уДачный Фермер': [24587, 4181, 'Курьером СММ']}

    # price_list = {'MegaPixel': [35980, 1, 'Курьером СММ', 1],
    pc = Price_Change(price_list, min_price=18990, max_price=21890, sensitivity=0, step=10).run()
    print('итог', pc)
