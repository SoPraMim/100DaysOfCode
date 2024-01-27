import requests

# --- Lesson 299 --- #
# response = requests.get(url="http://api.open-notify.org/iss-now.json")
# response.raise_for_status()

# data = response.json()
# longitude = data["iss_position"]["longitude"]
# latitude = data["iss_position"]["latitude"]
# coordinates = (longitude,latitude)
# print(coordinates)

# --- Lesson 301 --- #
parameters = {
    "lat":55.676098,
    "lng":12.568337,
    "formatted":0
}
response = requests.get(url="https://api.sunrise-sunset.org/json",params=parameters)
response.raise_for_status()
data = response.json()["results"]
print(data)