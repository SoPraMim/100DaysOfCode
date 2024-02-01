# --- Imports --- #
import os
import requests
from datetime import datetime

# --- Global Variables --- #

WEIGHT_KG = 90
HEIGHT_CM = 183
AGE = 34


NUTRITIONIX_ID = os.environ.get("NUTRITIONIX_ID")
NUTRITIONIX_API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")

nutritionix_host_domain = "https://trackapi.nutritionix.com"
nutritionix_nlfe_endpoint = f"{nutritionix_host_domain}/v2/natural/exercise"
sheety_endpoint = "https://api.sheety.co/b7e178e2a22198129738540deda58c52/myWorkouts/workouts"

date = datetime.now()

# --- Program --- #
header_params = {
    "x-app-id": NUTRITIONIX_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
}

sheety_header = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

params = {
    "query": input("Tell me which exercises you did: "),
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

request = requests.post(url=nutritionix_nlfe_endpoint,json=params, headers=header_params)
request.raise_for_status()
exercises = request.json()['exercises']

for exercise in exercises:
    sheety_params = {
        "workout": {
            "date": date.strftime("%d/%m/%Y"),
            "time": date.strftime("%H:%M:%S"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    
    request = requests.post(url=sheety_endpoint,headers=sheety_header,json=sheety_params)
    request.raise_for_status()