price_list = {'MegaPixel': [35890, 642, 'Курьером СММ', 1],
              'Мегамаркет Москва КГТ': [35990, 1, 'Курьером СММ'],
              'Фирменный магазин POLARIS Вешки (со склада МегаМаркет)': [37500, 15000, 'Курьером СММ'],
              'Фирменный магазин POLARIS СПб (со склада МегаМаркет)': [37600, 15000, 'Курьером СММ'],
              'Фирменный магазин POLARIS ЕКБ (со склада МегаМаркет)': [37900, 15000, 'Курьером СММ'],
              'ОГО! Онлайн-гипермаркет (DSM)': [60409, 605, 'Другие службы доставки'],
              'Техника в быту': [73917, 740, 'Курьером СММ'],
              'ИП Романова Татьяна Павловна': [82721, 828, 'Курьером СММ'],
              'RKStore': [113220, 1133, 'Курьером СММ'],
              'Магазин Polaris': [49990, 11499, 'Другие службы доставки'],
              'ОГО! Онлайн-гипермаркет (С&C)': [60409, 605, 'Другие службы доставки']}
old_my_price = price_list['MegaPixel']  # 'MegaPixel': [67990, 642, 'Доставка по клику, ', 1]
del price_list['MegaPixel']
price_list = [v for k, v in price_list.items() if 'Курьером СММ' in v]
all_prices = sorted(price_list, key=lambda x: x[0])
print(all_prices)

def adjust_prices(prices, max_price):
    new_price = max_price
    # Обходим каждый элемент в списке цен
    for i in range(len(prices)):
        # Если не первый элемент, сравниваем с предыдущим
        if i > 0:
            if abs(prices[i][0] - prices[i - 1][0]) > 1500:
                prices[i][0] = prices[i - 1][0] - 10
                return prices[i]
        # Если не последний элемент, сравниваем со следующим
        if i < len(prices) - 1:
            if abs(prices[i][0] - prices[i + 1][0]) > 1500:
                prices[i][0] = prices[i + 1][0] - 10
                return prices[i][0]
        print('new_price', new_price)
    return new_price

# теперь нужно прсчитать если будет один мой товар



# Пример списка цен
# prices = [35990, 37500, 37600, 37900]
prices = [[37490, 1, 'Курьером СММ']]

max_price = 38000
adjusted_prices = adjust_prices(prices, max_price)
print(adjusted_prices)


