from driver import installation
from parse import Parse_Page
from calculation.calculation_price import Price_Change


def new_price(url_smm, min_price, max_price, sensitivity, step, stock):
    useragent = installation()
    if stock:
        price_list = Parse_Page(url_smm, useragent).show_shop()
        if 'MegaPixel' not in price_list:
            # поставить сигнал боту что силениум не нашел наш магазин, хотя товар в наличии
            price_list = Parse_Page(url_smm, useragent).show_shop()
        return Price_Change(price_list, min_price, max_price, sensitivity, step).run()


