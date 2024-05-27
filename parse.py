import re

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from driver import installation, find_driver
from settings import min_rating


class Parse_Page:
    def __init__(self, url_smm, useragent):
        self.url_smm = url_smm
        self.price_list = {}
        self.useragent = useragent

    def _set_up(self):  # запускаем браузер
        self.driver = find_driver(self.useragent)
        self.driver.get(f'{self.url_smm}#?details_block=prices')

    def show_shop(self):
        self._set_up()
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        texts = soup.find_all('div', {'itemtype': 'http://schema.org/Offer'})
        for text in texts:
            bs = BeautifulSoup(str(text), 'lxml')
            shop = bs.find('span', {'class': 'pdp-merchant-rating-block__merchant-name'}).get_text(
                strip=True)
            price = int(re.sub(r"[\s,₽]", "", bs.find('span',
                                                     {'class': 'product-offer-price__amount'}).get_text(
                strip=True)))
            bonus = bs.find('span', {'class': 'bonus-amount'})
            bonus = int(bonus.get_text(strip=True).replace(' ', '')) if bonus else 0
            delivery_way = bs.find('div', {'class': 'offer-item-delivery-type'}).find('span').text
            delivery_date = bs.find('div', {'class': 'offer-item-delivery-type'}).find('span', {'class': 'offer-item-delivery-type__delivery-date'}).text
            delivery = delivery_way + delivery_date
            rating = bs.find('span', {'class': 'pdp-merchant-rating-block__rating'}).text.strip()
            if float(rating) > min_rating:
                print(delivery.lower())
                if 'курьером' in delivery.lower() or 'забрать' in delivery.lower() or 'час' in delivery.lower():
                    delivery = "Другие службы доставки"
                else:
                    delivery = "Курьером СММ"
                self.price_list[shop] = [price, bonus, delivery]
        return self.price_list


if __name__ == "__main__":
    useragent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    pr = Parse_Page('https://megamarket.ru/catalog/details/kofemashina-avtomaticheskaya-polaris-pacm-2060ac-100030226528_62654/#?details_block=prices', useragent).show_shop()
    print(pr)