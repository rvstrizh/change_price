from calculation.calculation_bonus import Calculation_Price_With_Bonus


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
            # Перебираем список, сравниваем элементы и выводим второй элемент, если разница больше 800
        for i in range(len(self.price_list) - 1):
            print(self.price_list[i + 1][0] - self.price_list[i][0])
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
    price_list = {'Интернет-гипермаркет "ТЕХНОСТОР" (ДСМ)': [41557, 6234, 'Другие службы доставки'], 'HOLODILNIK.RU (Север)': [40299, 6045, 'Курьером СММ'], 'ATmarket': [41419, 829, 'Курьером СММ'], 'Topcomputer.ru': [39852, 5978, 'Другие службы доставки'], 'OLDI': [40489, 14172, 'Другие службы доставки'], 'ОЛДИ': [41439, 829, 'Курьером СММ'], 'Evium': [38590, 9648, 'Курьером СММ'], 'Alt-Dim': [46190, 6929, 'Другие службы доставки'], 'Маркет Аврора': [41173, 8236, 'Курьером СММ'], 'MegaPixel': [37990, 7598, 'Курьером СММ'], 'Market Space': [38590, 9648, 'Курьером СММ'], 'Comboland': [42449, 8490, 'Курьером СММ'], 'BBSauto': [44365, 8874, 'Курьером СММ'], 'TopElectronics': [38449, 5768, 'Другие службы доставки'], 'Ситилинк Москва Доставка': [38590, 9263, 'Другие службы доставки'], 'super100k': [39488, 790, 'Курьером СММ'], 'ООО "Торговый Дом ОРИОН"': [39681, 794, 'Курьером СММ'], 'ИМПЕРИЯ ТЕХНО (ДСМ)': [39185, 5878, 'Другие службы доставки'], 'paimport.ru': [39488, 13822, 'Другие службы доставки'], 'AversPC': [40056, 802, 'Курьером СММ'], 'Кувалда.ру': [39590, 5939, 'Другие службы доставки'], 'Tehhouse': [40480, 810, 'Курьером СММ'], 'TK5': [40020, 6003, 'Другие службы доставки'], 'Мир Техники DBS': [40119, 6018, 'Другие службы доставки'], 'ImperiaTechno SPB': [41010, 821, 'Курьером СММ'], 'ИМПЕРИЯ ТЕХНО MSK': [41010, 821, 'Курьером СММ'], 'ИМПЕРИЯ ТЕХНО': [41010, 821, 'Курьером СММ'], 'NiceOneElectronics': [41070, 822, 'Курьером СММ'], 'Неватека': [41136, 823, 'Курьером СММ'], 'ЭЛЕТОРГ.РФ': [40896, 14315, 'Другие службы доставки'], 'Just.ru': [41489, 830, 'Курьером СММ'], 'Видеолайн DBS': [41800, 14630, 'Другие службы доставки'], 'Atbook': [42634, 853, 'Курьером СММ'], 'Видеолайн': [42830, 857, 'Курьером СММ'], 'SmartTechnology': [43431, 8688, 'Курьером СММ'], 'ПОЗИТРОНИКА': [44110, 6176, 'Курьером СММ'], 'TECHNO SMART': [44181, 8838, 'Курьером СММ'], 'ООО "ПРОСЕРВИС"': [45290, 9058, 'Курьером СММ'], 'kotofоto.ru': [45022, 4503, 'Курьером СММ'], 'kawaii': [45165, 4517, 'Курьером СММ'], 'ООО «Технопром»': [44610, 6692, 'Другие службы доставки'], 'ONLYBT.RU': [45218, 6783, 'Другие службы доставки'], 'Арсенал-БТ': [46260, 926, 'Курьером СММ'], 'Техно Фаворит': [46280, 6942, 'Другие службы доставки'], '2BIT.RU': [48518, 7278, 'Курьером СММ'], 'ЛИНИЯ': [48400, 21780, 'Другие службы доставки'], 'АКБ': [48400, 16940, 'Другие службы доставки'], 'MEGA': [48400, 21780, 'Другие службы доставки'], 'Just a store': [48990, 980, 'Курьером СММ'], 'AVTO-1': [48428, 16951, 'Другие службы доставки'], 'EXPERT': [48428, 16951, 'Другие службы доставки'], 'cenam.net (север)': [41859, 838, 'Курьером СММ'], 'CENAM.NET ( Юг )': [41859, 838, 'Курьером СММ'], 'ELEMENTX.Trade': [62609, 3131, 'Курьером СММ'], 'cenam.net ( запад )': [54630, 1093, 'Курьером СММ'], 'CENAM.NET (Москва)': [54630, 1093, 'Курьером СММ']}


    # price_list = {'MegaPixel': [35980, 1, 'Курьером СММ', 1],
    pc = Price_Change(price_list, min_price=36980, max_price=42000, sensitivity=1, step=10).run()
    print('итог', pc)
