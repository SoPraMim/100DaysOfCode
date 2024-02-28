from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import json
from target_manager import TargetManager
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
        self.resources = {}
        self.villages = {}
        self.resources_layout = {}
        self.buildings_layout = {}
        self.active_city = None
        self.targets = TargetManager()
        self.available_troops = {}
        self.__queue = []
        
        self.login()
        self.load_villages()
        self.update_active_city()
        self.update_resources()
    
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
        
    def update_resources(self):
        self.warehouse_capacity = self.driver.find_element(By.CSS_SELECTOR,".warehouse .capacity").text
        self.warehouse_capacity = int(self.warehouse_capacity.encode('ascii', errors='ignore').strip().decode('ascii').replace(",",""))
        self.granary_capacity = self.driver.find_element(By.CSS_SELECTOR,".granary .capacity").text
        self.granary_capacity = int(self.granary_capacity.encode('ascii', errors='ignore').strip().decode('ascii').replace(",",""))
        self.resources['wood'] = int(self.driver.find_element(By.CSS_SELECTOR,"#l1").text.replace(",",""))
        self.resources['clay'] = int(self.driver.find_element(By.CSS_SELECTOR,"#l2").text.replace(",",""))
        self.resources['iron'] = int(self.driver.find_element(By.CSS_SELECTOR,"#l3").text.replace(",",""))
        self.resources['crop'] = int(self.driver.find_element(By.CSS_SELECTOR,"#l4").text.replace(",",""))
        
    def update_villages(self):
        self.driver.find_element(By.CSS_SELECTOR,"#sidebarBoxVillagelist .header .buttonsWrapper a").click()
        time.sleep(WAIT_TIMER)
        n_villages = len(self.driver.find_elements(By.CSS_SELECTOR,"tbody tr"))
        for i in range(n_villages):
            village_name = self.driver.find_element(By.XPATH,f"/html/body/div[3]/div[3]/div[3]/div[2]/div/table/tbody/tr/td[{1+i}]/a").text
            self.villages[village_name] = {
                "resources_layout":{},
                "buildings_layout":{},
                "coordinates": [],
            }
            if village_name == "SPM 01":
                self.villages[village_name]["coordinates"] = [77,-41]
            self.identify_fields()
            self.identify_buildings()
            self.driver.find_element(By.CSS_SELECTOR,"#sidebarBoxVillagelist .header .buttonsWrapper a").click()
            time.sleep(WAIT_TIMER)
        self.save_villages()
        
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
        building_name = building_name.title()
        # if self.active_city != city_from:
        #     self.go_to_city(city_from)
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
        """Returns the id no of the building name. If more than one building is found returns  the least developed one."""
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
        possible_buildings ={key:item for key,item in buildings_list.items() if item['building'] == building_name.title()}
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
        #TODO Select a new village to control.
        pass

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
            for target in self.targets.get_targets(village):
                if not self.__check_cooldown_over(target):
                    print(f"Attack from {village} to {target['coordinates']} still in cooldown.")
                    continue
                if not self.__has_enough_troops(target):
                    print(f"Attack from {village} to {target['coordinates']} not performed due to lack of troops.")
                    continue
                if target['target_type'] == 'oasis' and not self.__is_target_empty(target):
                    print(f"Attack from {village} to {target['coordinates']} not performed due to oasis being occupied.")
                    continue
                self.attack_target(self.active_city,target)
                print(f"Attack from {village} to {target['coordinates']} sent.")
        return True
            
    def __has_enough_troops(self,target):
        self.update_available_troops()
        for key in self.available_troops:
            if self.available_troops[key]-target["troops"][key] < 0:
                return False
        else:
            return True
        
    def __check_cooldown_over(self,target:dict):
        last_attack = datetime.strptime(target['last_attack'],"%Y-%m-%d %H:%M:%S")
        cooldown = timedelta(minutes=target['cooldown'])
        return datetime.now() > last_attack + cooldown
        
    def __is_target_empty(self,target:dict):
        self.driver.get(target['target_url'])
        time.sleep(WAIT_TIMER)
        troop_info_element = self.driver.find_element(By.CSS_SELECTOR,"#troop_info")
        return "none" in troop_info_element.text
        
    def attack_target(self,city_from:str, target:dict,attack_type:str="raid"):
        """Send troops to target location."""
        self.driver.get("https://ts1.x1.international.travian.com/build.php?id=39&gid=16&tt=2")
        # if self.active_city != city_from:
        #     self.go_to_city(city_from)
        attack_value_codes = {
            "raid": "4",
            "normal":"3",
            "reinforcement":"5",
        }
        coordinates_x, coordinates_y = target["coordinates"]
        troops_required: dict = target["troops"]
        for troop,number_of_troops in troops_required.items():
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
        self.targets.update_last_attack(village_from=self.active_city, target= target)
        time.sleep(WAIT_TIMER)
        return True
    
    def improve_troop(self,city_from, troop:str):
        # if self.update_active_city() != city_from:
        #     self.go_to_village(city_from)
        
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
            print(f"{troop.title()} improved in {self.active_city}.")
            time.sleep(WAIT_TIMER)
            return True
        else:
            print(f"{troop.title()} in {city_from} cannot be improved yet.")
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
        # if self.update_active_city() != city_from:
        #     self.go_to_village(city_from)
        pass
        #TODO identify which building is required and go to the building.
        
        #TODO Identify the correct section for the troop.
        
        #TODO Check if you can create the troops and fill in the boxes if so.
        
        #TODO Confirm the troop creation
        
        
    # --- Queue Functions --- #
    
    def run_queue(self, timer:int=15):
        now = datetime.now()
        print("_______________________________")
        print(now.strftime('%Y-%m-%d %H:%M:%S'))
        if self.__last_reset + timedelta(minutes=75) < now:
            print("Driver has been running for too long. Resetting driver.")
            self.reset_driver()
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