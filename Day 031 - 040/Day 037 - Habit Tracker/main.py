import requests
from datetime import datetime
import os

USERNAME = "sopramim"
TOKEN = os.environ.get("PIXELA_USER_TOKEN")
GRAPH = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME, # MY_USERNAME
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH,
    "name": "Cycling Graph",
    "unit": "km",
    "type": "float",
    "color": "sora"
}
header = {
    "X-USER-TOKEN": TOKEN,
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=header)
# print(response.text)
today = datetime.today()

pixel_config = {
    "date":today.strftime("%Y%m%d"),
    "quantity": input("How many kilometers did you cycle today?")
}

# response = requests.post(url=f"{graph_endpoint}/{GRAPH}", json=pixel_config, headers=header)
# print(response.text)

new_pixel_data = {
    "quantity": "5"
}

# request = requests.put(url=f"{graph_endpoint}/{GRAPH}/{pixel_config['date']}",json=new_pixel_data, headers=header)
# print(response.text)

request = requests.delete(url=f"{graph_endpoint}/{GRAPH}/{pixel_config['date']}", json=new_pixel_data, headers=header)
