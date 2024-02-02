
class SearchFlightData:
    def __init__(self, iata_code_from, iata_code_to, max_price) -> None:
        self.city_from = iata_code_from
        self.city_to = iata_code_to
        self.max_price = max_price
        
class FlightData:
    def __init__(self,search_result:dict) -> None:
        data = search_result["data"][0]
        self.cityCodeFrom = data["cityCodeFrom"]
        self.cityFrom = data["cityFrom"]
        self.cityCodeTo = data["cityCodeTo"]
        self.cityTo = data["cityTo"]
        self.price = data["fare"]["adults"]
        self.deep_link = data["deep_link"]
        
        departure = data["utc_departure"].split("T")
        self.utc_departure_date = departure[0]
        self.utc_departure_time = departure[1][:5]
        
        arrival = data["utc_arrival"].split("T")
        self.utc_departure_date = arrival[0]
        self.utc_departure_time = arrival[1][:5]