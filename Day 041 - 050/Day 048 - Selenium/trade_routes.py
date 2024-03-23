from datetime import datetime
import json

ROOT = ""

class TradeRoutesManager:
    """Manages trade.json and keeps in memory recurrent trade routes."""
    def __init__(self) -> None:
        self.routes:dict = None
        
        self.load_targets()
        
    def load_targets(self):
        try:
            with open(f"{ROOT}trade.json","r") as file:
                self.routes = json.loads(file.read())
        except FileNotFoundError:
            self.routes = {}
    
    def save_routes(self):
        with open(f"{ROOT}trade.json", "w") as file:
            json.dump(self.routes,file,indent=4)
                
    def add_new_route(self,city_from:str, coordinates_to:list, resources:dict, cooldown:int=1440):
        if self.routes.get(city_from) is None:
            self.routes[city_from] = []
        self.routes[city_from].append({
            "coordinates": coordinates_to,
            "resources": resources,
            "cooldown": cooldown,
            "last_trade": "2024-01-01 00:00:00"
        })
        self.save_routes()
        
    def delete_route(self,city_from, idx):
        self.routes[city_from].pop(idx)
    
    def get_routes(self,city_from):
        try:
            return self.routes[city_from].copy()
        except KeyError:
            return []
        
    def reset_cooldown(self,city_from:str,trade_route):
        route_found = False
        for route in self.routes.get(city_from):
            if route == trade_route:
                route_found = True
                break
        now = datetime.now()
        route["last_trade"] = now.strftime("%Y-%m-%d %H:%M:%S")
        self.save_routes()
            
        