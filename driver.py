import tempfile
import contextlib
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import fake_useragent as fu
from bs4 import BeautifulSoup


def installation():
    while True:
        try:
            print('test')
            useragent = fu.UserAgent().random
            b = ChromeExtended(proxy="http://4ren8c:K1W9CM@193.124.177.248:9515", useragent=useragent)
            b.get("https://megamarket.ru")
            page = b.page_source
            soup = BeautifulSoup(page, 'lxml')
            pr = soup.find_all('div', {'class': 'header-logo'})
            if pr:
                print('stop')
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
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument(f"--load-extension={extensionDirpath}")
        options.add_argument(f'--user-agent={self.useragent}')


def find_driver(user_agent):
    driver = ChromeExtended(proxy="http://4ren8c:K1W9CM@193.124.177.248:9515", useragent=user_agent)
    return driver


