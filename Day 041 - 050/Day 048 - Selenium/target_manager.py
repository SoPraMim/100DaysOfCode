import json
from datetime import datetime
import math

ROOT = ""

class TargetManager:
    def __init__(self) -> None:
        self.targets={}
        
        self.load_targets()
    
    def add_new_target(self,village_from:str,target_url:str,target_name:str,
                       target_type:str,coordinates:list,troops:dict,cooldown:int):
        if self.targets.get(village_from) is None:
            self.targets[village_from] = []
        new_target = {
            "target_name": target_name,
            "target_type": target_type,
            "coordinates": coordinates,
            "troops": troops,
            "cooldown": cooldown,
            "last_attack": "2024-01-01 00:00:00",
            "target_url": target_url,
        }
        if self.target_exists(village_from,new_target):
            target_idx = self.get_target_idx_from_url(village_from,target_url)
            self.targets[village_from][target_idx] = new_target
        else:
            self.targets[village_from].append(new_target)
        self.save_targets()
        
    def save_targets(self):
        with open(f"{ROOT}targets.json", "w") as file:
            json.dump(self.targets,file,indent=4)
            
    def load_targets(self):
        try:
            with open(f"{ROOT}targets.json","r") as file:
                self.targets = json.loads(file.read())
        except FileNotFoundError:
            pass
        
    def get_targets(self,village_from:str):
        targets:list = self.targets.get(village_from)
        if targets == None:
            return []
        else:
            return targets.copy()
    
    
    def get_targets_coordinates(self,village_from):
        return [target["coordinates"] for target in self.get_targets(village_from)]
    
    def get_target_idx_from_url(self,village_from,target_url) -> int:
        for i in range(len(self.targets[village_from])):
            if self.targets[village_from][i]["target_url"] == target_url:
                return i
        
    def delete_target_by_idx(self,village_from,idx):
        self.targets[village_from].pop(idx)
        self.save_targets()
    
    def update_last_attack(self, village_from:str, target_coordinates:list):
        now = datetime.now()
        all_targets_from_city = self.get_targets(village_from)
        target_found = False
        for idx in range(len(all_targets_from_city)):
            if target_coordinates == all_targets_from_city[idx].get("coordinates"):
                target_found = True
                break
        if not target_found:
            return    
                    
        self.targets[village_from][idx]["last_attack"] = now.strftime("%Y-%m-%d %H:%M:%S")
        self.save_targets()
        
    def update_target_attribute(self,village_from, target,key,new_item):
        all_attacks_from_city = self.get_targets(village_from)
        idx = all_attacks_from_city.index(target)
        self.targets[village_from][idx][key] = new_item
        self.save_targets()
        
    def target_exists(self, village_from:str, target:dict) -> bool:
        """Checks if a target with the same coordinates exists."""
        all_targets_from_city = self.get_targets_coordinates(village_from)
        target_coordinates = list(target["coordinates"])
        return target_coordinates in all_targets_from_city

    def calculate_distance(self,coordinates_from, coordinates_to):
        x_from,y_from = coordinates_from
        x_to, y_to = coordinates_to
        x_dist = x_to - x_from
        y_dist = y_to - y_from
        dist = math.sqrt(x_dist**2 + y_dist**2) 
        return dist
    
    def sort_targets_by_dist(self,city_from:str,city_from_coordinates:list):
        targets:list = self.get_targets(city_from)
        new_targets = []
        while len(targets) > 0:
            for i in range(len(targets)):
                if i == 0:
                    lowest_dist = self.calculate_distance(city_from_coordinates,targets[i]["coordinates"])
                    idx_lowest_dist = 0
                    continue
                dist = self.calculate_distance(city_from_coordinates,targets[i]["coordinates"])
                if dist < lowest_dist:
                    lowest_dist = dist
                    idx_lowest_dist = i
            new_targets.append(targets[idx_lowest_dist])
            targets.pop(idx_lowest_dist)
        self.targets[city_from] = new_targets
        self.save_targets()