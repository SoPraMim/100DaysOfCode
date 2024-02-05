# --- Imports --- #
import os
import requests
import pandas as pd
from flight_search import FlightSearch
from generic_functions import cls,set_y_or_n

# --- Global Variables --- #
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_ENDPOINT = os.environ.get("FLIGHT_TRACKER_SHEETY_ENDPOINT")

# --- Headers --- #
SHEETY_HEADER = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

# --- Class --- #
class DataManager:
    def __init__(self) -> None:
        self.flights = None
        self.__users = None
        self.__header = SHEETY_HEADER
        self.flight_search = FlightSearch()
        
        request = requests.get(url=f"{SHEETY_ENDPOINT}flights", headers=self.__header)
        request.raise_for_status()
        self.flights = request.json()

        request = requests.get(url=f"{SHEETY_ENDPOINT}users", headers=self.__header)
        request.raise_for_status()
        self.__users = request.json()
    
    def check_codes(self) -> None:
        for i in range(len(self.flights["flights"])):
            params = {"flight": {}}
            if self.flights["flights"][i].get("iataCodeFrom") is None or self.flights["flights"][i].get("iataCodeFrom") == "":
                iataCodeFrom = self.flight_search.search_city(self.flights["flights"][i]["from"])
                self.flights["flights"][i]["iataCodeFrom"] = iataCodeFrom
                params["flight"]["iataCodeFrom"] = iataCodeFrom
            if self.flights["flights"][i].get("iataCodeTo") is None or self.flights["flights"][i].get("iataCodeTo") == "":
                iataCodeTo = self.flight_search.search_city(self.flights["flights"][i]["to"])
                self.flights["flights"][i]["iataCodeTo"] = iataCodeTo
                params["flight"]["iataCodeTo"] = iataCodeTo
            if params != {"flight": {}}:
                request = requests.put(url=f"{SHEETY_ENDPOINT}flights/{self.flights['flights'][i]['id']}", json=params, headers=self.__header)
                request.raise_for_status()
        
    def get_users(self) -> list:
        return self.__users["users"]
    
    def get_user_routes(self,user:dict) -> list:
        """Returns the flight routes from a given user."""
        user_id = user["userId"]
        return [self.flights["flights"][i] for i in range(len(self.flights["flights"])) if self.flights["flights"][i]["userId"] == user_id]  
    
    def create_new_route(self):
        cls()
        print("Welcome to Flight Club!\nWe find the best deals and email them to you.")
        #Select user
        e_mail = input("Type your e-mail.")
        for user in self.__users["users"]:
            if e_mail == user["eMail"]:
                if set_y_or_n(f"Are you {user['name']}? (Y/N)\n"):
                    user_id = user["userId"]
                    break
        else:
            print("User not found.")
            if set_y_or_n("Do you want to create a new user? (Y/N)\n"):
                user_id = self.create_new_user(e_mail)
        city_from = input("Where do you want to leave from?\n")
        city_to = input("Where do you want to go?\n")
        iata_code_from = self.flight_search.search_city(city_from)
        iata_code_to = self.flight_search.search_city(city_to)
        while True:
            try:
                max_price = int(input("How much are you willing to spend?\n"))
                break
            except:
                print("Wrong input. Please type a number.\n")
        new_route = {
            "flight": {
                "from": city_from,
                "iataCodeFrom": iata_code_from,
                "to": city_to,
                "iataCodeTo": iata_code_to,
                "maxPrice": max_price,
                "userId": user_id
            }
        }
        request = requests.post(url=f"{SHEETY_ENDPOINT}flights", json=new_route, headers=self.__header)
        request.raise_for_status()
        cls()
              
    def create_new_user(self, e_mail: str):
        name = input("What is your name?\n").title()
        user_id = self.__users["users"][-1]["userId"] + 1
        
        user = {        
            "name":name,
            "eMail":e_mail,
            "userId": user_id
        }
        params = {"user": user}
        request = requests.post(url=f"{SHEETY_ENDPOINT}users",json=params,headers=self.__header)
        request.raise_for_status()

        user["id"] =  self.__users["users"][-1]["id"] + 1
        self.__users["users"].append(user)
        return user_id