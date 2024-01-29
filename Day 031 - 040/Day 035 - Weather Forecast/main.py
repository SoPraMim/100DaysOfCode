# --- Imports --- #
import requests
import os
from generic_functions import send_mail

# --- Global Variables --- #
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
MY_LAT = 55.676098 # Your latitude
MY_LONG = -12.568337 # Your longitude
MY_KEY = os.environ.get("OMW_API_KEY")

# --- Program --- #
params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": MY_KEY,
    "cnt": 4
}

response = requests.get(url=OWM_ENDPOINT,params=params)
response.raise_for_status()
data = response.json()["list"]
weather_forecast_codes = [item["weather"][0]["id"] for item in data]
if any([weather_code < 700 for weather_code in weather_forecast_codes]):
    send_mail("It will rain today!","It will rain today.\nRemember to bring an umbrella!!!",[os.environ.get("TO_TEST_EMAIL")])