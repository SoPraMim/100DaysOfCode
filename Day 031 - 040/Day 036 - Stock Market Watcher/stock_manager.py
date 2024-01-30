import os
import requests
import pandas as pd
from data import DATA
from generic_functions import send_mail


class StockManager():
    def __init__(self, stock_code: str, company_name: str) -> None:
        self.stock_code = stock_code
        self.company_name = company_name
        self.data = None
        self.news = None
        self.request_data()
    
    def request_data(self):
        # --- Program --- #
        # STEP 1: Use https://www.alphavantage.co
        # When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": self.stock_code,
            "apikey": os.environ.get("ALPHA_VANTAGE_API_KEY"),
            "outputsize": "compact"
        }
        response = requests.get(url="https://www.alphavantage.co/query",params=params)
        response.raise_for_status()
        try:
            self.data = pd.DataFrame(response.json()["Time Series (Daily)"]).transpose()
        except:
            self.data = pd.DataFrame(DATA).transpose() # test data
            print("Run out of available API requests. Test data used.")
    
    def check_price_variation(self) -> float:
        closing_prices = self.data["4. close"]
        return ( float(closing_prices[0]) - float(closing_prices[1]) ) / float(closing_prices[1])
    
    def request_news(self):
        params = {
            "apiKey": os.environ.get("NEWSAPI_KEY"),
            "q": self.company_name,
            "language": "en",
            "sortBy": "publishedAt"
        }
        response = requests.get(url="https://newsapi.org/v2/everything",params=params)
        response.raise_for_status()
        self.news = response.json()["articles"][0:3]
        
    def send_news(self,recipients: list):
        price_variation = self.check_price_variation()
        if price_variation > 0:
            price_variation_symbol = "⬆️"
        elif price_variation < 0:
            price_variation_symbol = "⬇️"
        header =  f"{self.stock_code} {price_variation_symbol} {abs(price_variation)*100:.2f} %\n\n" # header

        message_body = header
        for news in self.news:
            headline = "Headline: " + news["title"] + "\n"
            brief = "Brief: " + news["description"] + "\n"
            url = "Link: " + news["url"] + "\n"
            message_body = message_body + "\n" + headline + brief + url
            
        send_mail(header,message_body,recipients)