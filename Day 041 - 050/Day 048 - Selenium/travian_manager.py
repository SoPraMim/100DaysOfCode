from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import json
from target_manager import TargetManager
from trade_routes import TradeRoutesManager
from datetime import datetime, timedelta
from typing import Callable

ROOT = ""
URL = "https://ts1.x1.international.travian.com/"
WAIT_TIMER = 1

class Travian:
    def __init__(self) -> None:
        self.driver = []
        self.__last_reset:datetime = None
        self.warehouse_capacity = 0
        self.granary_capacity = 0
        self.villages = {}
        self.resources_layout = {}
        self.buildings_layout = {}
        self.active_city = None
        self.targets = TargetManager()
        self.available_troops = {}
        self.__queue = []
        self.trade_routes = TradeRoutesManager()
        
        self.login()
        self.load_villages()
        self.update_active_city()
    
    # --- Driver-Related Functions --- #
    def login(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(URL)
        self.__last_reset = datetime.now()

        # Login
        self.driver.find_element(By.CSS_SELECTOR,".account input").send_keys(os.environ.get("TRAVIAN_ACCOUNT"))
        self.driver.find_element(By.CSS_SELECTOR,".pass input").send_keys(os.environ.get("TRAVIAN_PASSWORD"))
        self.driver.find_element(By.CSS_SELECTOR,".loginButtonRow button").click()
        time.sleep(3)
        
    def refresh(self):
        self.driver.refresh()
        
    def reset_driver(self):
        self.driver.quit()
        self.login()
        
    def get_last_reset(self):
        return self.__last_reset.strftime("%Y-%m-%d %H:%M:%S")
    
    # --- Village Management Functions --- #        
    def save_villages(self):
        with open(f"{ROOT}villages.json","w") as file:
            json.dump(self.villages,file,indent=4)
            
    def load_villages(self):
        try:
            with open(f"{ROOT}villages.json","r") as file:
                self.villages = json.loads(file.read())
        except FileNotFoundError:
            self.update_villages()
            
    def get_all_villages(self):
        return [village for village in self.villages]
        
    def check_resources(self):
        resources = {
            "Lumber": int(self.driver.find_element(By.CSS_SELECTOR,"#l1").text.replace(",","")),
            "Clay": int(self.driver.find_element(By.CSS_SELECTOR,"#l2").text.replace(",","")),
            "Iron": int(self.driver.find_element(By.CSS_SELECTOR,"#l3").text.replace(",","")),
            "Crop": int(self.driver.find_element(By.CSS_SELECTOR,"#l4").text.replace(",","")),
        }
        return resources

    def update_villages(self):
        village_list = self.driver.find_element(By.CSS_SELECTOR,".villageList")
        village_entries = village_list.find_elements(By.CSS_SELECTOR,".listEntry")
        for entry in village_entries:
            village_name = entry.find_element(By.CSS_SELECTOR,".name").text
            coordinates = entry.find_element(By.CSS_SELECTOR,".coordinates").text.replace("|",",").replace("−","-")
            coordinates = list(eval(coordinates.encode('ascii', errors='ignore').strip().decode('ascii')))
            
            self.villages[village_name] = {
                "resources_layout":{},
                "buildings_layout":{},
                "coordinates": coordinates,
            }
        for village in self.villages:
            self.go_to_village(village)
            self.identify_fields()
            self.identify_buildings()
        self.save_villages()
        self.go_to_resources_view()
        
    # def update_villages(self):
    #     self.driver.find_element(By.CSS_SELECTOR,"#sidebarBoxVillagelist .header .buttonsWrapper a").click()
    #     time.sleep(WAIT_TIMER)
    #     n_villages = len(self.driver.find_elements(By.CSS_SELECTOR,"tbody tr"))
    #     for i in range(n_villages):
    #         village_name = self.driver.find_element(By.XPATH,f"/html/body/div[3]/div[3]/div[3]/div[2]/div/table/tbody/tr/td[{1+i}]/a").text
    #         self.villages[village_name] = {
    #             "resources_layout":{},
    #             "buildings_layout":{},
    #             "coordinates": [],
    #         }
    #         if village_name == "SPM 01":
    #             self.villages[village_name]["coordinates"] = [77,-41]
    #         self.identify_fields()
    #         self.identify_buildings()
    #         self.driver.find_element(By.CSS_SELECTOR,"#sidebarBoxVillagelist .header .buttonsWrapper a").click()
    #         time.sleep(WAIT_TIMER)
    #     self.save_villages()
        
    def go_to_resources_view(self):
        self.driver.find_element(By.CSS_SELECTOR,".resourceView").click()
        time.sleep(WAIT_TIMER)
        
    def identify_fields(self):
        village_name = self.update_active_city()
        self.go_to_resources_view()
        for i in range(18):
            self.driver.find_element(By.CSS_SELECTOR,f".buildingSlot{i+1}").click()
            time.sleep(WAIT_TIMER)
            building_name = self.driver.find_element(By.CSS_SELECTOR,".titleInHeader")
            (resource,level) = building_name.text.split(" Level ")
            level = int(level)
            if self.__is_under_construction():
                level += 1
            self.villages[village_name]["resources_layout"][str(i+1)] = {
                "resource":resource,
                "level": level
            }
            self.driver.find_element(By.CSS_SELECTOR,".resourceView").click()
            time.sleep(WAIT_TIMER)
            
    def go_to_buildings_view(self):
        self.driver.find_element(By.CSS_SELECTOR,".buildingView").click()
        time.sleep(WAIT_TIMER)
        
    def identify_buildings(self):
        village_name = self.update_active_city()
        self.go_to_buildings_view()
        for i in range(22):
            try:
                if i == 21:
                    self.driver.get("https://ts1.x1.international.travian.com/build.php?id=40&gid=31")
                else:
                    self.driver.find_element(By.CSS_SELECTOR,f"#villageContent .a{19+i}").click()
                time.sleep(WAIT_TIMER)
                building = self.driver.find_element(By.CSS_SELECTOR,"h1").text
                (building_name,level) = building.split(" Level ")
                level = int(level)
                if self.__is_under_construction():
                    level += 1
                self.villages[village_name]["buildings_layout"][str(19+i)] = {
                            'building': building_name,
                            'level': level
                }
                self.driver.find_element(By.CSS_SELECTOR,".buildingView").click()
                time.sleep(WAIT_TIMER)

            except:
                self.villages[village_name]["buildings_layout"][str(19+i)] = {
                    'building': 'empty',
                    'level': 0
                }
                
    def __is_under_construction(self):
        """Tests whether the currently selected building is under construction."""
        try:
            self.driver.find_element(By.CSS_SELECTOR,".underConstruction")
            return True
        except:
            return False
                
    def improve_building(self,city_from:str, building_name:str):
        """Improves the building selected. If more than one building of the same name exists, improves the least developed one."""
        self.update_active_city()
        if self.active_city != city_from:
            self.go_to_village(city_from)
        building_id = self.__query_building(building_name)
        if building_id is None:
            raise ValueError("Building not found.")
        
        if building_name in ['Woodcutter','Clay Pit','Iron Mine','Cropland']:
            layout = "resources_layout"
            self.go_to_resources_view()
            self.driver.find_element(By.CSS_SELECTOR,f".buildingSlot{building_id}").click()
            time.sleep(WAIT_TIMER)
            
        else:
            layout = "buildings_layout"
            self.go_to_buildings_view()
            if building_id == "40":
                self.driver.get("https://ts1.x1.international.travian.com/build.php?id=40&gid=31")
            else:
                self.driver.find_element(By.CSS_SELECTOR,f"#villageContent .a{building_id}").click()
            time.sleep(WAIT_TIMER)
            
        upgrade_button = self.driver.find_element(By.XPATH,f"/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[3]/div[1]/button")
        text_to_check = " ".join(upgrade_button.text.split()[:3])
        if text_to_check == "Upgrade to level":
            upgrade_button.click()
            self.villages[self.active_city][layout][building_id]['level'] += 1
            self.save_villages()
            print(f"{building_name} in {city_from} has been improved")
            return True
        else:
            print(f"{building_name} in {city_from} cannot be improved yet")
            return False
        
    def __query_building(self,building_name:str):
        """Returns the id no of the building name. If more than one building is found returns the least developed one."""
        self.update_active_city()
        if building_name in ['Woodcutter','Clay Pit','Iron Mine','Cropland']:
            return self.__query_resources_layout(building_name)
        else:
            return self.__query_building_layout(building_name)
    
    def __query_resources_layout(self,building_name:str):
        """Returns the if of a resource field."""
        field_list:dict = self.villages[self.active_city]['resources_layout']
        possible_buildings ={key:item for key,item in field_list.items() if item['resource'] == building_name.title()}
        try:
            lowest_level = min([item['level'] for _,item in possible_buildings.items()])
        except ValueError:
            return None
        for key,item in possible_buildings.items():
            if item['level'] == lowest_level:
                return key

    def __query_building_layout(self,building_name:str):
        """Returns the id of a building"""
        buildings_list:dict = self.villages[self.active_city]['buildings_layout']
        possible_buildings ={key:item for key,item in buildings_list.items() if item['building'] == building_name}
        try:
            lowest_level = min([item['level'] for _,item in possible_buildings.items()])
        except ValueError:
            return None
        for key,item in possible_buildings.items():
            if item['level'] == lowest_level:
                return key
    
    def get_all_buildings(self,city_from:str) -> list:
        output_list = []
        village = self.villages[city_from]
        for _,resource_field in village["resources_layout"].items():
            if resource_field["resource"] == "empty":
                continue
            if resource_field["resource"] not in output_list:
                output_list.append(f"{resource_field['resource']}")
        for _,building_slot in village["buildings_layout"].items():
            if building_slot["building"] == "empty":
                continue
            if building_slot["building"] not in output_list:
                output_list.append(f"{building_slot['building']}")
        return output_list
    
    def update_active_city(self):
        """Updates the active city."""
        self.active_city = self.driver.find_element(By.CSS_SELECTOR,".villageInput").get_attribute("value")
        return self.active_city
    
    def go_to_village(self,new_city:str):
        self.update_active_city()
        if self.active_city == new_city:
            return
        village_list = self.driver.find_element(By.CSS_SELECTOR,".villageList")
        village_entries = village_list.find_elements(By.CSS_SELECTOR,".listEntry")
        for entry in village_entries:
            entry_text = entry.text
            if new_city in entry_text:
                break
        entry.find_element(By.TAG_NAME,"a").click()
        time.sleep(WAIT_TIMER)
        self.update_active_city()
        
    def get_coordinates(self, city:str) -> list:
        return self.villages[city]["coordinates"]

    # --- Attacks-Related Functions --- #    
    def add_target(self,village_from,target_url,target_name,target_type,troops,cooldown):
        if target_type not in ['village','oasis']:
            raise ValueError('Target type not available.')
        coordinate_x,coordinate_y = target_url.split("?")[1].split("&")
        coordinate_x = int(coordinate_x.replace("x=",""))
        coordinate_y = int(coordinate_y.replace("y=",""))
        coordinates = [coordinate_x,coordinate_y]
        cooldown = int(cooldown)
        self.targets.add_new_target(village_from=village_from, 
                                    target_url=target_url,
                                    target_name=target_name,
                                    target_type=target_type,
                                    coordinates=coordinates,
                                    troops=troops,
                                    cooldown=cooldown)
        self.targets.sort_targets_by_dist(city_from=village_from,city_from_coordinates=self.villages[village_from]["coordinates"])
        
    def delete_target_by_idx(self, city_from, idx):
        self.targets.delete_target_by_idx(city_from, idx)
        
        
    def get_targets(self,city_from:str):
        return self.targets.get_targets(city_from)
        
        
    def update_available_troops(self):
        """Updates the available troops in the city."""
        rally_point_url = "https://ts1.x1.international.travian.com/build.php?gid=16&tt=1&filter=3"
        if self.driver.current_url != rally_point_url:
            self.driver.get(rally_point_url)
            time.sleep(WAIT_TIMER)
        # Find the proper table and extract a list of troops.
        headers = self.driver.find_elements(By.TAG_NAME,"h4")
        for header in headers:
            if "Troops in this village" in header.text:
                break
        table = header.find_element(By.XPATH,"following-sibling::table")
        items = table.find_elements(By.CSS_SELECTOR, "td.unit")
        troops = [int(item.text) for item in items]
        self.available_troops = {
            'Legionnaire': troops[0],
            'Praetorian': troops[1],
            'Imperian': troops[2],
            'Equites Legati': troops[3],
            'Equites Imperatoris': troops[4],
            'Equites Caesaris': troops[5],
            'Battering ram': troops[6],
            'Fire Catapult': troops[7],
            'Senator': troops[8],
            'Settler': troops[9],
            'Hero': troops[10],
        }
        return self.available_troops
    
    def farm_targets(self):
        for village in self.villages:
            targets = self.targets.get_targets(village)
            for target in targets:
                try:
                    target = target.copy()
                    self.go_to_village(village)
                    # 1. check the cooldown
                    if not self.__target_cooldown_is_over(target):  
                        print(f"Attack from {village} to {target['coordinates']} still in cooldown.")
                        continue
                    
                    if target['target_type'] == 'oasis':
                        oasis_empty = self.__is_target_empty(target)
                        oasis_player_owned = self.is_player_owned(target)
                        
                        if not any([oasis_empty,oasis_player_owned]):
                            army_sent = False
                            # Send to hero to occupied nature oasis. 
                            if self.hero_in_village():
                                hero_hp = self.get_hero_hp()
                                if hero_hp > 50: # but only if the hero hp is above 50 %.
                                    target["troops"] = {
                                        "Legionnaire": 0,
                                        "Praetorian": 0,
                                        "Imperian": 0,
                                        "Equites Legati": 0,
                                        "Equites Imperatoris": 100,
                                        "Equites Caesaris": 0,
                                        "Battering ram": 0,
                                        "Fire Catapult": 0,
                                        "Senator": 0,
                                        "Settler": 0,
                                        "Hero": 1
                                    }
                                    self.attack_target(self.active_city,target_coordinates=target["coordinates"],troops=target["troops"],reset=True)
                                    print(f"Hero sent from {village} to clear Oasis in {target['coordinates']}.")
                                    army_sent = True
                                    continue
                            # Remaining conditions for occupied oasis 
                            test_armies = [{
                                "Legionnaire": 0,
                                "Praetorian": 0,
                                "Imperian": 0,
                                "Equites Legati": 0,
                                "Equites Imperatoris": 200,
                                "Equites Caesaris": 0,
                                "Battering ram": 0,
                                "Fire Catapult": 0,
                                "Senator": 0,
                                "Settler": 0,
                                "Hero": 0
                            },
                                {
                                "Legionnaire": 0,
                                "Praetorian": 0,
                                "Imperian": 300,
                                "Equites Legati": 0,
                                "Equites Imperatoris": 0,
                                "Equites Caesaris": 0,
                                "Battering ram": 0,
                                "Fire Catapult": 0,
                                "Senator": 0,
                                "Settler": 0,
                                "Hero": 0
                            }]
                            for army in test_armies:
                                target["troops"] = army
                                if self.__has_enough_troops(target):
                                    self.attack_target(self.active_city,target_coordinates=target["coordinates"],troops=target["troops"],reset=True)
                                    print(f"Clean up army sent from {village} to clear Oasis in {target['coordinates']}.")
                                    army_sent = True
                                    continue
                            if army_sent == False:
                                print(f"Clean up army not available to clear Oasis in {target['coordinates']}.")
                            continue
                                

                    # Normal Farm routine
                    # 2. Check if target is oasis
                    if target['target_type'] == 'oasis':
                        if oasis_player_owned:
                            print(f"Attack from {village} to {target['coordinates']} not performed due to oasis being conquered by a player.")
                            continue
                        if oasis_empty:
                            if not self.__has_enough_troops(target):     # Exit condition when the oasis is empty.
                                print(f"Attack from {village} to {target['coordinates']} not performed due to lack of troops.")
                                continue
                        elif not oasis_empty:
                            print(f"Attack from {village} to {target['coordinates']} not performed due to oasis being occupied.")
                            continue
                    
                    else: # If the target is not an oasis:
                        if not self.__has_enough_troops(target):
                            print(f"Attack from {village} to {target['coordinates']} not performed due to lack of troops.")
                            continue                    
                    self.attack_target(self.active_city,target_coordinates=target["coordinates"],troops=target["troops"])
                    print(f"Attack from {village} to {target['coordinates']} sent.")
                except:
                    print(f"*ERROR* Attack from {village} to {target['coordinates']} failed. This is likely due to village not existing.")
        return True
    
    def hero_in_village(self) -> bool:
        self.update_available_troops()
        return self.available_troops["Hero"] > 0
    
    def get_hero_hp(self):
        url = "https://ts1.x1.international.travian.com/hero/attributes"
        if self.driver.current_url != url:
            self.driver.get(url)
            time.sleep(WAIT_TIMER)
        hp = self.driver.find_element(By.CSS_SELECTOR,".attributeBox .stats .value").text.replace("%","")
        hp = hp.encode('ascii', errors='ignore').strip().decode('ascii')
        return int(hp)
            
    def __has_enough_troops(self,target):
        self.update_available_troops()
        for key in self.available_troops:
            if self.available_troops[key]-target["troops"][key] < 0:
                return False
        else:
            return True
        
    def __target_cooldown_is_over(self,target:dict):
        last_attack = datetime.strptime(target['last_attack'],"%Y-%m-%d %H:%M:%S")
        cooldown = timedelta(minutes=target['cooldown'])
        return datetime.now() > last_attack + cooldown
        
    def __is_target_empty(self,target:dict):
        if self.driver.current_url != target['target_url']:
            self.driver.get(target['target_url'])
            time.sleep(WAIT_TIMER)
        troop_info_element = self.driver.find_element(By.CSS_SELECTOR,"#troop_info")
        return "none" in troop_info_element.text
    
    def is_player_owned(self, target):
        """Check is oasis is owned by a player"""
        if self.driver.current_url != target['target_url']:
            self.driver.get(target['target_url'])
            time.sleep(WAIT_TIMER)
        try:
            self.driver.find_element(By.CSS_SELECTOR,"#village_info")
            return True # If it found the element
        except:
            return False
        
    def attack_target(self,city_from:str, target_coordinates:list,troops: dict, attack_type:str="raid",reset:bool=True):
        """Send troops to target location."""
        self.go_to_village(city_from)
        self.driver.get("https://ts1.x1.international.travian.com/build.php?id=39&gid=16&tt=2")
        attack_value_codes = {
            "raid": "4",
            "normal":"3",
            "reinforcement":"5",
        }
        coordinates_x, coordinates_y = target_coordinates
        for troop,number_of_troops in troops.items():
            if number_of_troops == 0:
                continue
            icon = self.driver.find_element(By.CSS_SELECTOR,f'td [alt="{troop}"]')
            input = icon.find_element(By.XPATH,"following-sibling::input")
            input.send_keys(str(number_of_troops))
        self.driver.find_element(By.CSS_SELECTOR,f'.xCoord input').send_keys(str(coordinates_x))
        self.driver.find_element(By.CSS_SELECTOR,f'.yCoord input').send_keys(str(coordinates_y))
        radio_button_group = self.driver.find_element(By.CSS_SELECTOR,f'.option')
        radio_button_group.find_element(By.CSS_SELECTOR, f'[value="{attack_value_codes[attack_type]}"]').click()
        self.driver.find_element(By.CSS_SELECTOR,f'[value="ok"]').click()
        time.sleep(WAIT_TIMER)
        self.driver.find_element(By.CSS_SELECTOR,f'[value="Confirm"]').click()
        if reset:
            self.targets.update_last_attack(city_from, target_coordinates)
        time.sleep(WAIT_TIMER)
        return True
    
    def improve_troop(self,city_from, troop:str):
        if self.update_active_city() != city_from:
            self.go_to_village(city_from)
        
        # go to smithy
        building_id = self.__query_building("Smithy")
        self.go_to_buildings_view()
        self.driver.find_element(By.CSS_SELECTOR,f"#villageContent .a{building_id}").click()
        time.sleep(WAIT_TIMER)
        # look for the correct "improve troop" button and validate the improvement 
        section = self.driver.find_elements(By.CSS_SELECTOR,".research")
        for div in section:
            if troop.title() in div.text:
                troop_div = div
        button = troop_div.find_element(By.CSS_SELECTOR,".information .cta button")
        if "Improve" in button.text:
            button.click()
            print(f"{troop} improved in {self.active_city}.")
            time.sleep(WAIT_TIMER)
            return True
        else:
            print(f"{troop} in {city_from} cannot be improved yet.")
            return False
        
    def find_crop(self,coordinates:tuple,radius:int, minimun_crops=9):
        (coordinate_x, coordinate_y) = coordinates
        for x in range(coordinate_x-radius, coordinate_x+radius+1, 1):
            for y in range(coordinate_y-radius, coordinate_y+radius+1, 1):
                self.driver.get(f"https://ts1.x1.international.travian.com/karte.php?x={x}&y={y}")
                time.sleep(WAIT_TIMER)
                try:
                    rows = self.driver.find_elements(By.CSS_SELECTOR,"#distribution tr")
                    for row in rows:
                        if "Crop" in row.text:
                            n_crops = int(row.text.split()[0])
                            if n_crops >= minimun_crops:
                                print(f"Field with {n_crops} crops found at ({x}|{y}).")
                except:
                    pass
                
    def create_troops(self,city_from:str,troop:str, n_troops):
        # identify which building is required and go to the building.
        if troop in ["Legionnaire","Praetorian", "Imperian"]:
            buildings_required = ["Barracks"]
        elif troop in ["Equites Legati", "Equites Imperatoris", "Equites Caesaris"]:
            buildings_required = ["Stable"]
        elif troop in ["Battering ram", "Fire Catapult"]:
            buildings_required = ["Workshop"]
        elif troop in ["Senator"]:
            buildings_required = ["Residence"]
        
        self.go_to_village(city_from)
        self.go_to_buildings_view()
        for building in buildings_required:
            building_id = self.__query_building(building)
            if building_id is not None:
                break
        if building_id is None:
            raise ValueError("Building not found.")
        self.driver.find_element(By.CSS_SELECTOR,f"#villageContent .a{building_id}").click()
        time.sleep(WAIT_TIMER)
            
        # Identify the correct section for the troop.
        troop_sections = self.driver.find_elements(By.CSS_SELECTOR,"#nonFavouriteTroops .troop")
        troop_not_found = True
        for troop_section in troop_sections:
            if troop in troop_section.text:
                troop_not_found = False
                n_troops_possible = troop_section.find_element(By.CSS_SELECTOR,".cta a")
                n_troops_possible = int(n_troops_possible.text)
                if n_troops <= n_troops_possible:
                    troop_input = troop_section.find_element(By.CSS_SELECTOR,".cta input")
                    troop_input.send_keys(Keys.CONTROL + "a")
                    troop_input.send_keys(Keys.DELETE)
                    troop_input.send_keys(str(n_troops))
                else: 
                    print(f"Not enough resources to train {troop}")
                    return False
        if troop_not_found:
            raise LookupError(f"Troop not found in {city_from}: {troop}")
        train_troops_btn = self.driver.find_element(By.CSS_SELECTOR,".startTraining")
        train_troops_btn.click()
        print(f"{n_troops} {troop} produced in {city_from}.")
        time.sleep(WAIT_TIMER)
        return True
        
        
    # --- Queue Functions --- #
    
    def run_queue(self, timer:int=15):
        now = datetime.now()
        print("_______________________________")
        print(now.strftime('%Y-%m-%d %H:%M:%S'))
        if self.__last_reset + timedelta(minutes=75) < now:
            print("Driver has been running for too long. Resetting driver.")
            self.reset_driver()
        self.update_active_city()
        for i in range(len(self.__queue)-1,-1,-1):
            task = self.__queue[i]
            handle = task[0]
            args = task[1]
            repeatable = task[2]
            try:
                function_executed = self.__execute_task(handle,args)
                if repeatable == False and function_executed:
                    self.__queue.pop(i)
            except:
                print(f"***ERROR*** Current task: {handle.__name__} | Args: {args} | Repeat = {repeatable}")
        self.go_to_resources_view()
        print("_______________________________")
        
    def __execute_task(self,handle:Callable,args:list):
        return handle(*args)
        
    def add_to_queue(self,task:Callable,args:list,repeatable:bool=False):
        self.__queue.insert(0,(task,args,repeatable))
        
    def get_queue(self) -> list:
        return self.__queue.copy()
    
    def delete_from_queue(self,task_idx):
        self.__queue.pop(task_idx)
    
    # --- Trade routes --- #
    
    def add_trade_route(self,city_from:str, coordinates_to:list, resources:dict, cooldown:int=1440):
        self.trade_routes.add_new_route(city_from, coordinates_to, resources, cooldown)
        
    def get_routes(self,city_from:str):
        return self.trade_routes.get_routes(city_from)
    
    def run_trade_routes(self):
        for village in self.get_all_villages():
            trade_routes = self.get_routes(village)
            for trade_route in trade_routes:
                self.go_to_village(village)
                if not self.__trade_route_cooldown_is_over(trade_route):
                    print(f"Trade route from {village} to {trade_route['coordinates']} is still on cooldown.")
                    continue
                if not self.__has_enough_resources(trade_route):
                    print(f"Not enough resources to send from {village} to {trade_route['coordinates']}.")
                    continue
                try:
                    self.send_merchants(city_from=village, coordinates_to=trade_route['coordinates'],resources=trade_route.get("resources"))
                    self.__reset_trade_route_cooldown(village, trade_route)
                    print(f"Resources sent from {village} to {trade_route['coordinates']}.")
                except:
                    raise
            
    def __trade_route_cooldown_is_over(self,trade_route:dict):
        last_trade = datetime.strptime(trade_route['last_trade'],"%Y-%m-%d %H:%M:%S")
        cooldown = timedelta(minutes=trade_route['cooldown'])
        return datetime.now() > last_trade + cooldown
    
    def __has_enough_resources(self,trade_route:dict) -> bool:
        available_resources:dict = self.check_resources()
        resources_needed:dict = trade_route.get("resources")
        for resource in available_resources:
            if (available_resources.get(resource) - resources_needed.get(resource)) < 0:
                return False
        else:
            return True
        
    def send_merchants(self,city_from:str, coordinates_to:list,resources:dict):
        self.go_to_village(city_from)
        self.go_to_buildings_view()
        building_id = self.__query_building("Marketplace")
        self.driver.find_element(By.CSS_SELECTOR,f"#villageContent .a{building_id}").click()
        time.sleep(WAIT_TIMER)
        top_row = self.driver.find_elements(By.CSS_SELECTOR,".favor")
        for element in top_row:
            if "Send resources" in element.text:
                element.click()
                break
        time.sleep(WAIT_TIMER)
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".coordinateX input").send_keys(str(coordinates_to[0]))
            self.driver.find_element(By.CSS_SELECTOR, ".coordinateY input").send_keys(str(coordinates_to[1]))
            self.driver.find_element(By.CSS_SELECTOR, "input[name='lumber']").send_keys(str(resources["Lumber"]))
            self.driver.find_element(By.CSS_SELECTOR, "input[name='clay']").send_keys(str(resources["Clay"]))
            self.driver.find_element(By.CSS_SELECTOR, "input[name='iron']").send_keys(str(resources["Iron"]))
            self.driver.find_element(By.CSS_SELECTOR, "input[name='crop']").send_keys(str(resources["Crop"]))
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            return True
        except:
            return False
        
    def __reset_trade_route_cooldown(self, city_from, trade_route):
        self.trade_routes.reset_cooldown(city_from,trade_route)
        
    
    # --- Other functions --- #
