import re

from bs4 import BeautifulSoup

from settings import min_rating, CaptchaError


class Parse_Page_SMM:
    def __init__(self, url_smm, useragent):
        self.url_smm = url_smm
        self.price_list = {}
        self.useragent = useragent

    def _set_up(self):  # запускаем браузер
        self.driver = find_driver(self.useragent)
        self.driver.get(f'{self.url_smm}#?details_block=prices')

    def show_shop(self):
        self._set_up()
        self.driver.execute_script("window.stop();")
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        captcha_smm = soup.find_all('div', {'class': 'header-logo'})
        if not captcha_smm:
            print('мое исключение')
            raise CaptchaError('Вылезла капча')
        texts = soup.find_all('div', {'itemtype': 'http://schema.org/Offer'})
        for text in texts:
            bs = BeautifulSoup(str(text), 'lxml')
            try:
                shop = bs.find('span', {'class': 'pdp-merchant-rating-block__merchant-name'}).get_text(
                    strip=True)
                rating = bs.find('span', {'class': 'pdp-merchant-rating-block__rating'}).text.strip()
            except AttributeError as f: # если название магазина "выгодное предложение" оно как картинка а не текст
                shop = 'Выгодное предложение!'
                rating = 5
            price = int(re.sub(r"[\s,₽]", "", bs.find('span',
                                                     {'class': 'product-offer-price__amount'}).get_text(
                strip=True)))
            bonus = bs.find('span', {'class': 'bonus-amount'})
            bonus = int(bonus.get_text(strip=True).replace(' ', '')) if bonus else 0
            delivery_way = bs.find('div', {'class': 'offer-item-delivery-type'}).find('span').text
            delivery_date = bs.find('div', {'class': 'offer-item-delivery-type'}).find('span', {'class': 'offer-item-delivery-type__delivery-date'}).text
            delivery = delivery_way + delivery_date
            if float(rating) > min_rating:
                if 'курьером' in delivery.lower() or 'забрать' in delivery.lower() or 'час' in delivery.lower():
                    delivery = "Другие службы доставки"
                else:
                    delivery = "Курьером СММ"
                self.price_list[shop] = [price, bonus, delivery]
        if not self.price_list:
            try:
                shop = soup.find('span', {'class': 'pdp-merchant-rating-block__merchant-name'}).get_text(
                    strip=True)
                price = soup.find('span', {'class': 'sales-block-offer-price__price-final'}).get_text(
                    strip=True).replace(' ', '')[:-1]
                self.price_list[shop] = [int(price), 1, 'Курьером СММ']
            except AttributeError:
                pass
        return self.price_list


class Parse_Page_YM:
    def __init__(self, url_ym, useragent):
        self.url_ym = url_ym
        self.price_list = {}
        self.useragent = useragent

    def _set_up(self):  # запускаем браузер
        self.driver = find_driver(self.useragent)
        self.driver.get(f'{self.url_ym}#?details_block=prices')

    def show_shop(self):
        self._set_up()
        self.driver.execute_script("window.stop();")
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        pr = soup.find_all('div', {'class': 'lR763'})
        if not pr:
            print('мое исключение')
            raise CaptchaError('Вылезла капча')
        texts = soup.find_all('div', {'class': '_3-Y--'})
        print(texts)
        for text in texts:
            print(text)
            bs = BeautifulSoup(str(text), 'lxml')
            shop = bs.find('span', {'class': '_3Vzm8'}).get_text(
                    strip=True)
            print(shop)
            # price = int(re.sub(r"[\s,₽]", "", bs.find('span',
            #                                          {'class': 'product-offer-price__amount'}).get_text(
            #     strip=True)))
            # delivery_way = bs.find('div', {'class': 'offer-item-delivery-type'}).find('span').text
            # delivery_date = bs.find('div', {'class': 'offer-item-delivery-type'}).find('span', {'class': 'offer-item-delivery-type__delivery-date'}).text
            # delivery = delivery_way + delivery_date

        # if not self.price_list:
        #     try:
        #         shop = soup.find('span', {'class': 'pdp-merchant-rating-block__merchant-name'}).get_text(
        #             strip=True)
        #         price = soup.find('span', {'class': 'sales-block-offer-price__price-final'}).get_text(
        #             strip=True).replace(' ', '')[:-1]
        #         self.price_list[shop] = [int(price), 1, 'Курьером СММ']
        #     except AttributeError:
        #         pass
        # return self.price_list


if __name__ == "__main__":
    useragent = 'Mozilla/5.0 (Linux; Android 11; moto e20 Build/RONS31.267-94-14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36'
    for i in range(3):
        try:
            pr = Parse_Page_YM(f'https://market.yandex.ru/product--smartfon-samsung-galaxy-a15-4g/44500479/offers?cpa=1&how=aprice&grhow=supplier&sku=102627410013&uniqueId=62878861&local-offers-first=0{"&how=aprice"}', useragent).show_shop()
            print(pr)
        except CaptchaError:
            useragent = installation(f'https://market.yandex.ru/product--smartfon-samsung-galaxy-a15-4g/44500479/offers?cpa=1&how=aprice&grhow=supplier&sku=102627410013&uniqueId=62878861&local-offers-first=0{"&how=aprice"}')

# https://market.yandex.ru/product--smartfon-samsung-galaxy-a15-4g/44500479/offers?grhow=supplier&sku=102627410013&uniqueId=62878861&how=aprice&local-offers-first=0
# https://market.yandex.ru/product--smartfon-samsung-galaxy-a15-4g/44500479/offers?grhow=supplier&sku=102627410013&uniqueId=62878861&local-offers-first=0