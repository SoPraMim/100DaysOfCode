import json
from datetime import datetime

ROOT = ""

class TargetManager:
    def __init__(self) -> None:
        self.targets={}
        
        self.load_targets()
    
    def add_new_target(self,village_from:str,target_url:str,target_name:str,
                       target_type:str,coordinates:tuple,troops:dict,cooldown:int):
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
            raise KeyError("Target already exists")
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
        return self.targets[village_from]
    
    def get_targets_coordinates(self,village_from):
        return [target["coordinates"] for target in self.get_targets(village_from)]
    
    def delete_target(self,village_from,idx):
        self.targets[village_from].pop(idx)
        self.save_targets()
    
    def update_last_attack(self,village_from,target):
        now = datetime.now()
        all_attacks_from_city = self.get_targets(village_from)
        idx = all_attacks_from_city.index(target)
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
