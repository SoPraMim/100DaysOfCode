from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import json
from target_manager import TargetManager
from datetime import datetime, timedelta

ROOT = ""
URL = "https://ts1.x1.international.travian.com/"
WAIT_TIMER = 2

class Travian:
    def __init__(self) -> None:
        self.driver = []
        self.warehouse_capacity = 0
        self.granary_capacity = 0
        self.resources = {}
        self.villages = {}
        self.resources_layout = {}
        self.buildings_layout = {}
        self.active_city = None
        self.targets = TargetManager()
        self.available_troops = {}
        
        self.login()
        self.load_villages()
        self.update_active_city()
        self.update_resources()
    
    def login(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(URL)

        # Login
        self.driver.find_element(By.CSS_SELECTOR,".account input").send_keys(os.environ.get("TRAVIAN_ACCOUNT"))
        self.driver.find_element(By.CSS_SELECTOR,".pass input").send_keys(os.environ.get("TRAVIAN_PASSWORD"))
        self.driver.find_element(By.CSS_SELECTOR,".loginButtonRow button").click()
        time.sleep(3)
    
    def export_villages(self):
        with open(f"{ROOT}villages.json","w") as file:
            json.dump(self.villages,file,indent=4)
            
    def load_villages(self):
        try:
            with open(f"{ROOT}villages.json","r") as file:
                self.villages = json.loads(file.read())
        except FileNotFoundError:
            self.update_villages()
        
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
                "buildings_layout":{}
            }
            self.identify_fields()
            self.identify_buildings()
            self.driver.find_element(By.CSS_SELECTOR,"#sidebarBoxVillagelist .header .buttonsWrapper a").click()
            time.sleep(WAIT_TIMER)
        self.export_villages()

    def identify_fields(self):
        village_name = self.update_active_city()
        self.driver.find_element(By.CSS_SELECTOR,".resourceView").click()
        time.sleep(WAIT_TIMER)
        for i in range(18):
            self.driver.find_element(By.CSS_SELECTOR,f".buildingSlot{i+1}").click()
            time.sleep(WAIT_TIMER)
            building_name = self.driver.find_element(By.CSS_SELECTOR,".titleInHeader")
            (resource,level) = building_name.text.split(" Level ")
            level = int(level)
            if self.is_under_construction():
                level += 1
            self.villages[village_name]["resources_layout"][str(i+1)] = {
                "resource":resource,
                "level": level
            }
            self.driver.find_element(By.CSS_SELECTOR,".resourceView").click()
            time.sleep(WAIT_TIMER)
            
    def identify_buildings(self):
        village_name = self.update_active_city()
        self.driver.find_element(By.CSS_SELECTOR,".buildingView").click()
        time.sleep(WAIT_TIMER)
        for i in range(22):
            try:
                self.driver.find_element(By.CSS_SELECTOR,f"#villageContent .a{19+i}").click()
                time.sleep(WAIT_TIMER)
                building = self.driver.find_element(By.CSS_SELECTOR,"h1").text
                (building_name,level) = building.split(" Level ")
                level = int(level)
                if self.is_under_construction():
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
                
    def is_under_construction(self):
        """Tests whether the currently selected building is under construction."""
        try:
            self.driver.find_element(By.CSS_SELECTOR,".underConstruction")
            return True
        except:
            return False
                
    def improve_building(self,building_name:str):
        """Improves the building selected. If more than one building of the same name exists, improves the least developed one."""
        building_name = building_name.title()
        building_id = self.query_building(building_name)
        if building_id is None:
            raise ValueError("Building not found.")
        if building_name in ['Woodcutter','Clay Pit','Iron Mine','Cropland']:
            layout = "resources_layout"
            self.driver.find_element(By.CSS_SELECTOR,".resourceView").click()
            time.sleep(WAIT_TIMER)
            self.driver.find_element(By.CSS_SELECTOR,f".buildingSlot{building_id}").click()
            time.sleep(WAIT_TIMER)
            
        else:
            layout = "buildings_layout"
            self.driver.find_element(By.CSS_SELECTOR,".buildingView").click()
            time.sleep(WAIT_TIMER)
            self.driver.find_element(By.CSS_SELECTOR,f"#villageContent .a{building_id}").click()
            time.sleep(WAIT_TIMER)
        upgrade_button = self.driver.find_element(By.XPATH,f"/html/body/div[3]/div[3]/div[3]/div[2]/div/div/div[3]/div[3]/div[1]/button")
        text_to_check = " ".join(upgrade_button.text.split()[:3])
        if text_to_check == "Upgrade to level":
            upgrade_button.click()
            self.villages[self.active_city][layout][building_id]['level'] += 1
            self.export_villages()
        else:
            raise LookupError("Building cannot be upgraded")
        
    def query_building(self,building_name:str):
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
    
    def update_active_city(self):
        """Updates the active city."""
        self.active_city = self.driver.find_element(By.CSS_SELECTOR,".villageInput").get_attribute("value")
        return self.active_city

    def add_target(self):
        village_from = self.active_city
        target_url = input("Copy-paste the url to the target:\n")
        # https://ts1.x1.international.travian.com/karte.php?x=77&y=-40
        target_name = input("Type the target name:\n")
        target_type = input("What kind of target is it? (village,oasis)\n")
        if target_type not in ['village','oasis']:
            raise ValueError('Target type not available.')
        coordinate_x,coordinate_y = target_url.split("?")[1].split("&")
        coordinate_x = int(coordinate_x.replace("x=",""))
        coordinate_y = int(coordinate_y.replace("y=",""))
        coordinates = (coordinate_x,coordinate_y)
        coordinates = tuple([int(coordinate) for coordinate in coordinates])
        troops = {
            'Legionnaire': int(input("Number of Legionnaires: ")),
            'Praetorian': int(input("Number of Praetorians: ")),
            'Imperian': int(input("Number of Imperians:")),
            'Equites Legati': int(input("Number of Equites Legati: ")),
            'Equites Imperatoris': int(input("Number of Equites Imperatoris: ")),
            'Equites Caesaris': int(input("Number of Equites Caesaris: ")),
            'Battering ram': int(input("Number of Battering rams: ")),
            'Fire Catapult': int(input("Number of Fire Catapulst: ")),
            'Senator': int(input("Number of Senators: ")),
            'Settler': int(input("Number of Settlers: ")),
            'Hero': int(input("Number of Heros: ")),
        }
        cooldown = eval(input("How long between attacks (in minutes)?"))
        self.targets.add_new_target(village_from=village_from, 
                                    target_url=target_url,
                                    target_name=target_name,
                                    target_type=target_type,
                                    coordinates=coordinates,
                                    troops=troops,
                                    cooldown=cooldown)
        self.targets.save_targets()
        
        
    def update_available_troops(self):
        """Updates the available troops in the city."""
        rally_point_url = "https://ts1.x1.international.travian.com/build.php?id=39&gid=16&tt=1"
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
        now = datetime.now()
        print("_______________________________")
        print(now.strftime('%Y-%m-%d %H:%M:%S'))
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
                self.attack_target(target)
                print(f"Attack from {village} to {target['coordinates']} sent.")
            
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
        
    def attack_target(self,target:dict,attack_type:str="raid"):
        """Send troops to target location."""
        self.driver.get("https://ts1.x1.international.travian.com/build.php?id=39&gid=16&tt=2")
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

        