import tempfile
import contextlib
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import fake_useragent as fu
from bs4 import BeautifulSoup

from settings import login_proxy, password_proxy, proxy


def installation(market="https://megamarket.ru"):
    count = 0
    while True:

        try:
            count += 1
            print(f'test-{count}')
            useragent = fu.UserAgent().random
            b = ChromeExtended(proxy=f"http://{login_proxy}:{password_proxy}@{proxy}", useragent=useragent)

            b.get(market)
            b.save_screenshot(f'{count}.png')
            page = b.page_source
            soup = BeautifulSoup(page, 'lxml')
            if "https://megamarket.ru" in market:
                pr = soup.find_all('div', {'class': 'header-logo'})
            else:
                pr = soup.find_all('a', {'aria-label': 'Yandex'})
                if not pr:
                    print('stop')
                    print(useragent)
                    return useragent
            if pr:
                print('stop')
                print(useragent)
                return useragent
            time.sleep(3)
        except Exception as ex:
            print(ex)


class ChromeExtended(webdriver.Chrome):
    def __init__(self, *args, options=None, proxy=None, useragent=None, **kwargs):
        self.useragent = useragent
        options = options or Options()
        if proxy:
            context = tempfile.TemporaryDirectory()
        else:
            context = contextlib.nullcontext()

        with context as extensionDirpath:
            self._setupProxy(extensionDirpath, proxy, options)

            super().__init__(*args, options=options, **kwargs)

    def _setupProxy(self, extensionDirpath, proxy, options):
        # user_agent = fu.UserAgent().random
        # print(user_agent)
        # self.user_agent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
        if not proxy:
            return

        parsedProxy = urlparse(proxy)

        manifest_json = '{"version":"1.0.0","manifest_version":2,"name":"Chrome Proxy","permissions":["proxy","tabs","unlimitedStorage","storage","<all_urls>","webRequest","webRequestBlocking"],"background":{"scripts":["background.js"]},"minimum_chrome_version":"22.0.0"}'
        background_js = 'var e={mode:"fixed_servers",rules:{singleProxy:{scheme:"%s",host:"%s",port:parseInt(%s)},bypassList:["localhost"]}};chrome.proxy.settings.set({value:e,scope:"regular"},(function(){})),chrome.webRequest.onAuthRequired.addListener((function(e){return{authCredentials:{username:"%s",password:"%s"}}}),{urls:["<all_urls>"]},["blocking"]);' \
            % (parsedProxy.scheme, parsedProxy.hostname, parsedProxy.port, parsedProxy.username, parsedProxy.password)

        with open(f"{extensionDirpath}/manifest.json", "w", encoding="utf8") as f:
            f.write(manifest_json)
        with open(f"{extensionDirpath}/background.js", "w", encoding="utf8") as f:
            f.write(background_js)
        options.page_load_strategy = 'eager'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        # options.add_argument(f"--load-extension={extensionDirpath}")
        options.add_argument(f'--user-agent={self.useragent}')


def find_driver(user_agent):
    driver = ChromeExtended(proxy=f"http://{login_proxy}:{password_proxy}@{proxy}", useragent=user_agent)
    return driver


if __name__ == "__main__":
    installation('https://market.yandex.ru/?wprid=1722793746428774-16974013121432865173-balancer-l7leveler-kubr-yp-vla-31-BAL&utm_source_service=web&clid=703&src_pof=703&icookie=02hw1ZTZVrpJzWj657WRpext3VK7q%2FdmX9xE0stJ4dEdIt%2FEquK3UIt%2BKfrYH6cKTfu5XGMpWADMzbvMmIXdheDvPLg%3D&baobab_event_id=lzfuwziw7b')