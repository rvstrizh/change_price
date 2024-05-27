
price_thresholds = {3000: 0, 15000: 500, 15001: 1000}  # если кешбек выше у конкурента и цена до 3000 не меняем цену, если до 15000 делаем 500, если еще больше то 1000


class Calculation_Price_With_Bonus:
    def __init__(self, old_my_price, list_property, my_price, min_price):
        self.old_my_price = old_my_price
        self.list_property = list_property
        self.my_price = my_price
        self.min_price = min_price
        self.final_price = my_price

    def run(self):
        if self.old_my_price[1] == 1:
            return self.final_price
        my_price_including_bonus = (self.old_my_price[1] * 100) / self.old_my_price[0]
        price_including_bonus = (self.list_property[1] * 100) / self.list_property[0]
        difference_bonus = int(my_price_including_bonus) - int(price_including_bonus)
        # дописать если наш кешбек на много больше

        if difference_bonus < 0:
            for price, discont in price_thresholds.items():
                if self.list_property[0] > price and self.my_price - discont > self.min_price:
                    self.final_price = self.my_price - discont
        return self.final_price


if __name__ == "__main__":
    old_my_price = [1, 1, 'Доставка по клику, ', 1]
    list_property = [35890, 1, 'Курьером СММ']
    cp = Calculation_Price_With_Bonus(old_my_price, list_property, 35880, 34000).run()
    print(cp)