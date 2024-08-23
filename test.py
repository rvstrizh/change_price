# code below tested & working as of Nov 2023

# module versions used in example below
# selenium==4.14.0
# selenium-wire==5.1.0
# webdriver-manager==4.0.1

from seleniumwire import webdriver
from bs4 import BeautifulSoup

SCRAPEOPS_API_KEY = 'Ye19a7a05-ee1e-4fed-ad48-e7cfe824044a'
NUM_RETRIES = 2

proxy_options = {
    'proxy': {
        'http': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'https': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'no_proxy': 'localhost:127.0.0.1'
    }
}

## Store The Scraped Data In This List
scraped_quotes = []

## Urls to Scrape
url_list = [
    f'https://market.yandex.ru/product--smartfon-samsung-galaxy-a15-4g/44500479/offers?cpa=1&how=aprice&grhow=supplier&sku=102627410013&uniqueId=62878861&local-offers-first=0{"&how=aprice"}',
    f'https://market.yandex.ru/product--smartfon-samsung-galaxy-a15-4g/44500479/offers?cpa=1&how=aprice&grhow=supplier&sku=102627410013&uniqueId=62878861&local-offers-first=0{"&how=aprice"}',
    f'https://market.yandex.ru/product--smartfon-samsung-galaxy-a15-4g/44500479/offers?cpa=1&how=aprice&grhow=supplier&sku=102627410013&uniqueId=62878861&local-offers-first=0{"&how=aprice"}',
]

## Optional --> define Selenium options
option = webdriver.ChromeOptions()
option.add_argument('--headless')  ## --> comment out to see the browser launch.
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')
option.add_argument('--blink-settings=imagesEnabled=false')

## Set up Selenium Chrome driver
driver = webdriver.Chrome(
    options=option,
    seleniumwire_options=proxy_options)


### Our Helper Functions ###
def get_page_url_status_code(url, driver):
    page_url_status_code = 500

    # Access requests via the `requests` attribute
    for request in driver.requests:

        if request.response:
            # show all urls that are requested per page load
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type']
            )

        if request.url == url:
            page_url_status_code = request.response.status_code

    return page_url_status_code


## customise this list with what ever your page does not need
def interceptor(request):
    # stopping images from being requested
    # in case any are not blocked by imagesEnabled=false in the webdriver options above
    if request.path.endswith(('.png', '.jpg', '.gif')):
        request.abort()

    # stopping css from being requested
    if request.path.endswith(('.css')):
        request.abort()

    # stopping fonts from being requested
    if 'fonts.' in request.path:  # eg fonts.googleapis.com or fonts.gstatic.com
        request.abort()


### End Of Helper Functions ###


## looping through our list of urls
for url in url_list:

    ## manage retries in case we get a 500/401 response etc
    for _ in range(NUM_RETRIES):
        try:
            ## add an interceptor to make sure we don't request un-needed files (css or images) - saves money!
            driver.request_interceptor = interceptor

            driver.get(url)
            driver.save_screenshot('123.png')
            status_code = get_page_url_status_code(url, driver)

            if status_code in [200, 404]:
                ## escape for loop if the API returns a successful response
                break
        except Exception as e:
            print("error", e)
            driver.close()

    if status_code == 200:
        ## Feed HTML response into BeautifulSoup
        html_response = driver.page_source
        soup = BeautifulSoup(html_response, "html.parser")

        ## Find all quotes sections
        quotes_sections = soup.find_all('div', class_="quote")

        ## loop through each quotes section and extract the quote and author
        for quote_block in quotes_sections:
            quote = quote_block.find('span', class_='text').text
            author = quote_block.find('small', class_='author').text

            ## Add scraped data to "scraped_quotes" list
            scraped_quotes.append({
                'quote': quote,
                'author': author
            })

print(scraped_quotes)
