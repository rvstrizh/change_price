
price_thresholds = {4000: 0, 15000: 500, 40000: 1000, 70000: 1500, 100000: 2000, 100001: 3000}  # если кешбек выше у конкурента и цена до 3000 не меняем цену, если до 15000 делаем 500, если еще больше то 1000


class Calculation_Price_With_Bonus:
    def __init__(self, old_my_price, list_property, my_price, min_price):
        self.old_my_price = old_my_price
        self.list_property = list_property
        self.my_price = my_price
        self.min_price = min_price
        self.final_price = my_price

    def run(self):
        if self.old_my_price[0] == 1:
            if self.final_price < self.min_price:
                return self.min_price
            else:
                return self.final_price
        my_price_including_bonus = (self.old_my_price[1] * 100) / self.old_my_price[0]
        price_including_bonus = (self.list_property[1] * 100) / self.list_property[0]
        difference_bonus = int(my_price_including_bonus) - int(price_including_bonus)

        if difference_bonus < 0:
            print('ok')
            for price, discont in price_thresholds.items():
                if self.list_property[0] > price and self.my_price - discont > self.min_price:
                    self.final_price = self.my_price - discont
        elif difference_bonus > 0:
            # дописать если наш кешбек на много больше
            self.final_price = self.list_property[0] + (self.list_property[1] * my_price_including_bonus) / 100
        if self.final_price > 4000 and self.final_price == self.my_price and difference_bonus < 0 and self.final_price > self.min_price:
            self.final_price = self.min_price
        return int(self.final_price)


if __name__ == "__main__":
    old_my_price = [35980, 1, 'Курьером СММ', 1]
    list_property = [42657, 2260, 'Курьером СММ']
    cp = Calculation_Price_With_Bonus([34970, 700, 'Курьером СММ'], [34980, 700, 'Курьером СММ'], 34970, 30990).run()
    print(cp)