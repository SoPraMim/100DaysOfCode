import requests

class ISS():
    def __init__(self) -> None:
        self.latitude = None
        self.longitude = None
        self.update_position()

    def is_close(self,latitude,longitude):
        return abs(self.latitude - latitude) < 5 and abs(self.longitude - longitude) < 5
    
    def update_position(self):
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()

        self.latitude = float(data["iss_position"]["latitude"])
        self.longitude = float(data["iss_position"]["longitude"])
        
    def get_postion(self):
        return (self.latitude,self.longitude)