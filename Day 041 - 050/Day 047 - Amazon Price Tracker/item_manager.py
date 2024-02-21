import json
from generic_functions import set_y_or_n
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ROOT = "Day 041 - 050/Day 047 - Amazon Price Tracker/"


class ItemManager:
    def __init__(self) -> None:
        """Constructor of the ItemManager object. It automatically loads the list of items to track from file or creates the file if needed."""
        self.items = {}
        
        try:
            with open(f"{ROOT}product_list.json", "r") as file:
                self.items = json.loads(file.read())
        except FileNotFoundError:
            pass
    
    
    def add_item(self):
        """Add an item to the list of items to track."""
        product_name = input("Which product would you like to track?\n")
        if self.items.get(product_name) is not None and set_y_or_n(f"{product_name} already exists. Would you like to update it? (Y/N)\n"):
            return
        
        product_url = input("Paste the url to the product.\n")
        product_reference_price = float(input("At which price do you want to be notified?\n"))

        self.items[product_name] = {
                "url":product_url,
                "price":{},
                "reference_price": product_reference_price,
                }
            
        
    def delete_item(self,item:str):
        self.items.pop(item)
        self.save_data()
        
    def save_data(self):
        """Save the list of items to track to file."""
        with open(f"{ROOT}product_list.json", "w") as file:
            json.dump(self.items,file,indent=4)
            
    def check_price(self,item:str) -> float:
        """Update the price for a given item."""
        # Web scraping to get price.
        self.__validate_item(item)
        today = datetime.today()
        
        soup = self.__get_soup(self.items[item]["url"])
        price = soup.find(class_="a-offscreen").getText()
        currency = soup.find(class_="a-price-symbol").getText()
        price_without_currency = float(price.split(currency)[1])
        
        self.items[item]["price"][today.strftime("%Y-%m-%d")] = price_without_currency
        return price_without_currency  
    
    def get_items(self):
        return list(self.items.keys())
    
    def get_item_url(self,item:str):
        self.__validate_item(item)
        return self.items[item]["url"]
    
    def get_reference_price(self,item:str) -> float:
        self.__validate_item(item)
        return self.items[item]["reference_price"]
    
    def get_item_current_price(self,item):
        self.__validate_item(item)
        today = datetime.today()
        return self.items[item]["price"][today.strftime("%Y-%m-%d")]

    
    def __get_soup(self,url):
        ua = UserAgent()
        attempts = 1
        while True:
            ua_random = ua.random
            header = {
                "User-Agent": ua_random,
                "Accept-Language": "en-GB,en;q=0.9,pt-PT;q=0.8,pt;q=0.7,en-US;q=0.6",
            }
            request = requests.get(url=url,headers=header)
            request.raise_for_status()
            soup = BeautifulSoup(request.text, "lxml")
            
            if 'captcha' in str(soup):
                print(f"Bot detected. Attempt no: {attempts}. UA: {ua_random}")
                attempts += 1
                continue
            else:
                print(f"Protection bypassed.")
                return soup

    def __validate_item(self,item:str):
        if self.items.get(item) is None:
            raise ValueError("Item not found.")