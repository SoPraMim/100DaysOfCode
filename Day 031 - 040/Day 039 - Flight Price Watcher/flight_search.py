import requests
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flight_data import SearchFlightData

KIWI_HOST = "https://api.tequila.kiwi.com"

class FlightSearch:
    def __init__(self) -> None:
        self.__api_key = os.environ.get("KIWI_API_KEY")
    
    def search_city(self, city:str) -> list:
        header = {
            "apikey": self.__api_key,
        }
        
        params = {
            "term": city,
        }
        request = requests.get(url=f"{KIWI_HOST}/locations/query",params=params,headers=header)
        request.raise_for_status()
        response = request.json()["locations"]
        answers = [airport["code"] for airport in response]
        return answers[0]
    
    def search_flights(self,flight: SearchFlightData):
        
        endpoint = f"{KIWI_HOST}/v2/search"
        now = datetime.today()
        in_6_months = now + relativedelta(months=6)
        
        header = {
            "apikey": self.__api_key,
        }
        
        params = {
            "fly_from": flight.city_from,
            "fly_to": flight.city_to,
            "date_from": now.strftime("%d/%m/%Y"),
            "date_to": in_6_months.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 14,
            "ret_from_diff_city": False,
            "ret_to_diff_city": False,
            "adults": 1,
            "max_stopovers": 0,
            "one_for_city": 1,
            "price_to": flight.max_price
            
        }
        
        request = requests.get(url=endpoint, params=params, headers=header)
        request.raise_for_status()
        data = request.json()
        return data
        
        