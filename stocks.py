from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

def scrape_stock_data(symbol, exchange):
    ua = UserAgent()
    random_user_agent = ua.random
    if exchange == "NASDAQ":
        url = f"https://finance.yahoo.com/quote/{symbol}"
    elif exchange == "NSE":
        url = f"https://finance.yahoo.com/quote/{symbol}.NS/"
    custom_headers = {
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"
        'authority': 'www.dickssportinggoods.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        "User-Agent": random_user_agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
    }
    print(f"url ==> {url}")

    try:
        response = requests.get(url, headers=custom_headers)
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Yahooファイナンス
            # url = f"https://finance.yahoo.co.jp/quote/{symbol}"
            # current_price = soup.find(class_="PriceBoard__priceBlock__1PmX").find(class_="StyledNumber__value__3rXW").text

            # Yahoo Finance
            current_price = soup.find(attrs={'data-testid':'qsp-price'}).text
            price_changed = soup.find(attrs={'data-testid':'qsp-price-change'}).text
            percentage_changed = soup.find(attrs={'data-testid':'qsp-price-change-percent'}).text
            previous_close = soup.find(attrs={'data-field':'regularMarketPreviousClose'}).text
            week_52 = soup.find(attrs={'data-field':'fiftyTwoWeekRange'}).text.split("-")
            week_52_high = week_52[0].strip()
            week_52_low = week_52[1].strip()
            market_cap = soup.find(attrs={"data-field": "marketCap"}).text
            pe_ratio = soup.find(attrs={"data-field": "trailingPE"}).text
            dividend_yield = soup.find(attrs={"title": "Forward Dividend & Yield"}).find_next_sibling('span').text

            info = {
                "current_price": current_price,
                "price_changed": price_changed,
                "percentage_changed": percentage_changed,
                "previous_close": previous_close,
                "week_52_high": week_52_high,
                "week_52_low": week_52_low,
                "market_cap": market_cap,
                "pe_ratio": pe_ratio,
                "dividend_yield": dividend_yield,
            }
            print(f"info {symbol} ==> {info}")
            return info
        
    except Exception as e:
        print(f"Error scraping the data: {e}")
        return None
    

scrape_stock_data("TSLA", "NASDAQ")


    # current_price = models.CharField(max_length=25, null=True, blank=True)
    # price_changed = models.CharField(max_length=25, null=True, blank=True)
    # percentage_changed = models.CharField(max_length=25, null=True, blank=True)
    # previous_close = models.CharField(max_length=25, null=True, blank=True)
    # week_52_high = models.CharField(max_length=25, null=True, blank=True)
    # week_52_low = models.CharField(max_length=25, null=True, blank=True)
    # market_cap = models.CharField(max_length=25, null=True, blank=True)
    # pe_ratio = models.CharField(max_length=25, null=True, blank=True)
    # dividend_yield = models.CharField(max_length=25, null=True, blank=True)
