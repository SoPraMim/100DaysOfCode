import requests
from datetime import datetime

class TimeManager():
    def __init__(self,lat,long):
            self.__lat = lat
            self.__long = long
            self.__sunrise = None
            self.__sunset = None
            self.time_now = None 
            self.update_sunrise_sunset()

    def update_sunrise_sunset(self):
        parameters = {
            "lat": self.__lat,
            "lng": self.__long,
            "formatted": 0,
        }
        
        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
        data = response.json()
        self.__sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        self.__sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
        self.time_now = datetime.now()
        self.time_now = datetime(year=2024,month=1,day=27,hour=19)
        
    def is_dark(self):
        return self.time_now.hour < self.__sunrise or self.time_now.hour > self.__sunset