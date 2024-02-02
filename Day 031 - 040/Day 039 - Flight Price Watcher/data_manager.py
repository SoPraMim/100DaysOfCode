# --- Imports --- #
import os
import requests
import pandas as pd
from flight_search import FlightSearch
from flight_data import SearchFlightData

# --- Global Variables --- #
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_ENDPOINT = "https://api.sheety.co/b7e178e2a22198129738540deda58c52/flightTracker/flights"

# --- Headers --- #
sheety_header = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

class DataManager:
    def __init__(self) -> None:
        self.data = None
        self.df = None
        self.flight_search = FlightSearch()
        
        request = requests.get(url=SHEETY_ENDPOINT, headers=sheety_header)
        request.raise_for_status()
        self.data = request.json()
        self.df = pd.DataFrame(self.data["flights"])
        self.search_codes()

        
    def get_departures(self) -> list:
        return [row["from"] for row in self.data["flights"]]
    
    def search_codes(self):
        for i in range(self.df.shape[0]):
            self.df.loc[i,"iataCodeFrom"] = self.flight_search.search_city(self.df.loc[i,"from"])
            self.df.loc[i,"iataCodeTo"] = self.flight_search.search_city(self.df.loc[i,"to"])
            
    def get_flight_data(self) -> list:
        return [SearchFlightData(self.df.loc[i,"iataCodeFrom"],self.df.loc[i,"iataCodeTo"],self.df.loc[i,"maxPrice"]) for i in range(self.df.shape[0])]