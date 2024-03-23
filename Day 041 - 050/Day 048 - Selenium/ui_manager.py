# --- IMPORTS --- #
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from travian_manager import Travian
import math

# --- GLOBAL VARIABLES ---#

ROOT = "Day 041 - 050/Day 048 - Selenium/"
TROOPS_NAMES =[
    'Legionnaire',
    'Praetorian',
    'Imperian',
    'Equites Legati',
    'Equites Imperatoris',
    'Equites Caesaris',
    'Battering ram',
    'Fire Catapult',
    'Senator',
    'Settler',
    'Hero',
]


# --- USER INTERFACE --- #
class MainWindow:
    def __init__(self) -> None:                  
        self.queue_timer = None
        
        # Window
        self.root = Tk()
        self.root.title("Travian Controller")

        # Background
        self.canvas = Canvas(
            self.root,
            width=400,
            height=400,
            highlightthickness=0,
            bg= "#B2CCF2"
        )
        self.bg_img = Image.open(f"{ROOT}./images/Background.png", mode='r')
        self.bg_img = self.bg_img.resize((400, 400))
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.canvas.create_image(0, 0, image= self.bg_img, anchor= "nw")
        self.title = self.canvas.create_text(200,30, text="Travian Controller", fill="Black", font=("Arial", 25, "bold"))
        self.canvas.pack(fill="both",expand=True)

        # Buttons
        # Left collumn
        self.update_villages_btn = Button(
            self.root,
            text='Update Villages', 
            width=13,
            height=2, 
            command=TRAVIAN.update_villages
        )
        self.update_villages_btn.place(x=20, y=300)

        
        self.start_queue_btn = Button(
            self.root,
            text='Start Queue', 
            width=13,
            height=2, 
            command=self.__start_queue
        )
        self.start_queue_btn.place(x=280, y=300)

        self.manage_queue_btn = Button(
            self.root,
            text="Manage Queue",
            width=13,
            height=2,
            command=self.__open_queue_manager
        )
        self.manage_queue_btn.place(x=280, y=250)

        self.set_targets_btn = Button(
            self.root,
            text="Set Targets",
            width=13,
            height=2,
            command=self.__open_target_manager
        )
        self.set_targets_btn.place(x=280, y=200)
        
        self.set_trade_routes_btn = Button(
            self.root,
            text="Trade Routes",
            width=13,
            height=2,
            command=self.__open_trade_route_manager
        )
        self.set_trade_routes_btn.place(x=280, y=150)

        self.root.mainloop()

    # --- COMMANDS --- #
    def __start_queue(self):
        self.start_queue_btn.configure(text = "Stop Queue", command=self.__stop_queue)
        TRAVIAN.run_queue()
        wait_time = 15*60*1000
        self.queue_timer = self.root.after(wait_time, self.__start_queue)
        
    def __stop_queue(self):
        self.start_queue_btn.configure(text = "Start Queue", command=self.__start_queue)
        self.root.after_cancel(self.queue_timer)
        
    def __open_queue_manager(self):
        QueueManagerUI()
        
    def __open_target_manager(self):
        TargetManagerUI()
        
    def __open_trade_route_manager(self):
        TradeRouteManagerUI()
        
class QueueManagerUI:
    def __init__(self,) -> None:
        self.queue:list = []
        global TRAVIAN

        # Window
        self.root = Toplevel()
        self.root.title("Manage Queue")
        self.root.config(
            padx=10,
            pady=10,
            highlightthickness=0
        )
        
        # Tasklist
        self.list_box = Listbox(
            self.root,
            height=10,
            width=30,
            selectmode="SINGLE"
        )
        self.list_box.grid(
            padx=0,
            pady=0,
            column=0,
            row=0,
            rowspan=8,
            sticky=W+E+N+S
        )
        self.listbox_scrollbar = Scrollbar(self.root)
        self.listbox_scrollbar.grid(
            column=1,
            row=0,
            rowspan=8,
            sticky=W+E+N+S,
            padx=(0,20)
        )
        self.list_box.config(yscrollcommand = self.listbox_scrollbar.set)
        self.listbox_scrollbar.config(command = self.list_box.yview) 
        self.fill_task_list()

            
        # Dropdown Menus        
        self.village_label = Label(
            self.root,
            text="Select Village:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=20
        )
        self.village_label.grid(column= 2, row=0,padx=0,sticky=W+E+N+S)

        village_list = TRAVIAN.get_all_villages() # get the list of villages
        self.village_dropdown = ttk.Combobox(self.root,values=village_list)
        self.village_dropdown.grid(column=2,row=1,sticky=W+E+N+S)
        self.village_dropdown.bind("<<ComboboxSelected>>",self.update_queue_form)
        
        tasks = [
            "Farm targets",
            "Enable trade routes",
            "Improve a building",
            "Create troops"
        ]
        self.task_label = Label(self.root,
                               text="Select Task:", 
                               fg="Black",
                               font=("Arial",10,"normal"),
                               justify= "center",
                               width=20)
        self.task_label.grid(column= 2, row=3,padx=0,sticky=W+E+N+S)
        self.task_dropdown = ttk.Combobox(self.root,values=tasks)
        self.task_dropdown.grid(column=2,row=4,sticky=W+E+N+S)
        self.task_dropdown.bind("<<ComboboxSelected>>",self.update_queue_form)

        # Create troops form
        self.troop_name_label = Label(
            self.root,
            text="Select Troop:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=20
        )
        self.troop_name_label.grid(column=3,row=0,sticky=W+E+N+S)
        self.troop_name_dropdown = ttk.Combobox(self.root,values=TROOPS_NAMES)
        self.troop_name_dropdown.grid(column=3,row=1,sticky=W+E+N+S)
        
        self.troop_number_label = Label(
            self.root,
            text="Amount:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=20
        )
        self.troop_number_label.grid(column=3,row=3,sticky=W+E+N+S)
        self.troop_number_entry = Entry(
            self.root,
            width=20,
            justify="center"
        )
        self.troop_number_entry.grid(column=3,row=4,sticky=W+E+N+S)

        # Improve building form
        self.building_label = Label(self.root,
                               text="Select Building:", 
                               fg="Black",
                               font=("Arial",10,"normal"),
                               justify= "center",
                               width=20)
        self.building_label.grid(column=3,row=0,sticky=W+E+N+S)
        self.building_dropdown = ttk.Combobox(self.root,values=[" "])
        self.building_dropdown.grid(column=3,row=1,sticky=W+E+N+S)
    
        
        # Buttons
        self.add_to_queue_btn = Button(
            self.root,
            text='Add to Queue', 
            width=13,
            height=2,
            command=self.add_to_queue_btn_pressed
        )
        self.add_to_queue_btn.grid(column=0,row=8, columnspan=2)
        
        self.delete_from_queue_btn = Button(
            self.root,
            text='Delete Task', 
            width=13,
            height=2,
            command=self.delete_from_queue
        )
        self.delete_from_queue_btn.grid(column=2,row=8)
        
        for row in range(8):
           self.root.rowconfigure(row,minsize=20)
        self.update_queue_form()
        
        self.root.mainloop()
    
    def fill_task_list(self):
        self.list_box.delete(0,END)
        task_list = TRAVIAN.get_queue()
        task_list.reverse()
        if task_list == []:
            return
        for item in task_list:
            text = f"{item[0].__name__}({','.join([str(arg) for arg in item[1]])})"
            if item[2] == True:
                text += ", Repeat"
            self.list_box.insert(END, text)
                
    def update_queue_form(self,event=None):
        task_selection = self.task_dropdown.get()

        # Erasing boxes
        self.troop_name_label.grid_remove()
        self.troop_name_dropdown.grid_remove()
        self.troop_number_label.grid_remove()
        self.troop_number_entry.grid_remove()
        self.building_label.grid_remove()
        self.building_dropdown.grid_remove()

        if task_selection == "Improve a building":
            # Setting new values 
            village = self.village_dropdown.get()
            list_buildings=TRAVIAN.get_all_buildings(village)
            self.building_dropdown.configure(values=list_buildings)
            self.building_label.grid()
            self.building_dropdown.grid()
            
        if task_selection == "Create troops":
            self.troop_name_label.grid()
            self.troop_name_dropdown.grid()
            self.troop_number_label.grid()
            self.troop_number_entry.grid()
            
                     
    def add_to_queue_btn_pressed(self):
        # Get values from form.
        village = self.village_dropdown.get()
        task_selection = self.task_dropdown.get()
        # Tasks that do not require a village.
        if task_selection == "":
            return
        elif task_selection == "Farm targets":
            TRAVIAN.add_to_queue(TRAVIAN.farm_targets,[],repeatable=True)
        elif task_selection == "Enable trade routes":
            TRAVIAN.add_to_queue(TRAVIAN.run_trade_routes,[],repeatable=True)
            pass
        # Check that village is filled.
        elif village == "":
            return
        # Other tasks
        elif task_selection == "Improve a building":
            building_selection = self.building_dropdown.get()
            if building_selection == "":
                return
            TRAVIAN.add_to_queue(TRAVIAN.improve_building,[village,building_selection])
        elif task_selection == "Create troops":
            troop_name_selection = self.troop_name_dropdown.get()
            troop_number_selection = int(self.troop_number_entry.get())
            if troop_name_selection == "":
                return
            if troop_number_selection <= 0:
                return
            TRAVIAN.add_to_queue(TRAVIAN.create_troops,[village,troop_name_selection,troop_number_selection])
                
        self.fill_task_list()
        
    def delete_from_queue(self):
        current_selection = self.list_box.curselection()[0]
        queue = TRAVIAN.get_queue()
        correct_idx = len(queue) - current_selection - 1
        TRAVIAN.delete_from_queue(correct_idx)
        self.fill_task_list()
    
class TargetManagerUI:
    def __init__(self) -> None:
        # Atributes

        # Window
        self.root = Toplevel()
        self.root.title("Manage Queue")
        self.root.config(
           
            padx=10,
            pady=10,
            highlightthickness=0
        )
        
        # Target List
        self.list_box = Listbox(self.root,
                                height=10,
                                width=40,
                                selectmode="SINGLE")
        self.list_box.grid(
            padx=0,
            pady=0,
            column=0,
            row=0,
            rowspan=11,
            sticky=W+E+N+S
        )
        self.listbox_scrollbar = Scrollbar(self.root)
        self.listbox_scrollbar.grid(column=1,row=0, rowspan=11,sticky=W+E+N+S,padx=(0,20))
        self.list_box.config(yscrollcommand = self.listbox_scrollbar.set)
        self.listbox_scrollbar.config(command = self.list_box.yview)
        self.list_box.bind("<<ListboxSelect>>",self.update_form) 
        
        # Permanent Buttons
        self.village_label = Label(
            self.root,
            text="Select Village:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=20
        )
        self.village_label.grid(column= 2, row=0,padx=0,sticky=W+E+N+S)

        village_list = TRAVIAN.get_all_villages() # get the list of villages
        self.village_dropdown = ttk.Combobox(self.root,values=village_list)
        self.village_dropdown.grid(column=2,row=1,sticky=W+E+N+S)
        self.village_dropdown.bind("<<ComboboxSelected>>",self.update_target_list)
        
        
        self.add_target_btn = Button(
            self.root,
            text='Add/Edit Target', 
            width=13,
            height=2,
            command=self.add_target
        )
        self.add_target_btn.grid(column=2,row=3,rowspan=3,padx=20, sticky=W+E+N+S)
        
        self.delete_target_btn = Button(
            self.root,
            text='Delete Target', 
            width=13,
            height=2,
            command=self.delete_target
        )
        self.delete_target_btn.grid(column=2,row=7,rowspan=3,padx=20, sticky=W+E+N+S)
        
        # Form
        self.url_label = Label(self.root,
            text="URL:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=20)
        self.url_entry = Entry(self.root,width=40,justify="center")
        self.url_entry.insert(END, string="",)
        
        self.target_name_label = Label(
            self.root,
            text="Target Name:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=20
        )
        self.target_name_entry = Entry(self.root,width=40,justify="center")
        self.target_name_entry.insert(END, string="",)
        
        self.target_type_label = Label(
            self.root,
            text="Target Type:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=20
        )
        self.target_type_dropdown = ttk.Combobox(self.root,values=["Oasis","Village"])
        
        self.cooldown_label = Label(
            self.root,
            text="Time between attacks (min):", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=20
        )
        self.cooldown_entry = Entry(self.root,width=40,justify="center")
        

        self.troop_name_labels = []
        self.troop_entries = []
        for i in range(len(TROOPS_NAMES)):
            self.troop_name_labels.append(
                Label(
                    self.root,
                    text=TROOPS_NAMES[i], 
                    fg="Black",
                    font=("Arial",10,"normal"),
                    justify="right",
                    width=20
                )
            )
            self.troop_entries.append(
                Entry(self.root,width=10,justify="center")
            )
            self.troop_entries[i].insert(END, string="0",)

        for row in range(12):
            self.root.rowconfigure(row,minsize=22)
            
        self.url_label.grid(column= 3, row=0, rowspan=1, padx=0,sticky=W+E+N+S)
        self.url_entry.grid(column= 3, row=1, rowspan=1, sticky=W+E+N+S)
        self.target_name_label.grid(column= 3, row=3,rowspan=1, padx=0,sticky=W+E+N+S)
        self.target_name_entry.grid(column= 3, row=4,rowspan=1, padx=0,sticky=W+E+N+S)
        self.target_type_label.grid(column= 3, row=6,rowspan=1, padx=0,sticky=W+E+N+S)
        self.target_type_dropdown.grid(column= 3, row=7, rowspan=1, padx=0,sticky=W+E+N+S)
        self.cooldown_label.grid(column= 3, row=9, rowspan=1, padx=0,sticky=W+E+N+S)
        self.cooldown_entry.grid(column= 3, row=10, rowspan=1, padx=0,sticky=W+E+N+S)
        
        for i in range(len(self.troop_entries)):
            self.troop_name_labels[i].grid(column= 4, row=i, padx=0,sticky=W+E+N+S)
            self.troop_entries[i].grid(column= 5, row=i, padx=0,sticky=W+E+N+S)
            
        self.add_target_btn.configure(command=self.add_target)    
        
        # Fill empty fields
        self.update_target_list(None)
    
    def update_form(self,event):
        city = self.village_dropdown.get()
        target_text:str = self.list_box.get(ANCHOR)
        if target_text == "":
            self.empty_form()
            return
        coordinates = target_text.split("[")[-1].split("]")[0]
        coordinates = eval(f"[{coordinates}]")
        
        targets = TRAVIAN.get_targets(city)
        for target in targets:
            if target["coordinates"] == coordinates:
                break
        
        
        self.url_entry.delete(0,END)
        self.url_entry.insert(END,target["target_url"])
        self.target_name_entry.delete(0,END)
        self.target_name_entry.insert(END,target["target_name"])
        if target["target_type"] == "oasis":
            self.target_type_dropdown.current(0)
        elif target["target_type"] == "village":
            self.target_type_dropdown.current(1)    
        self.cooldown_entry.delete(0,END)
        self.cooldown_entry.insert(END,str(target["cooldown"]))
        
        for i in range(len(self.troop_entries)):
            self.troop_entries[i].delete(0,END)
            self.troop_entries[i].insert(END,target["troops"][TROOPS_NAMES[i]])
        
    def empty_form(self):
        """empty form"""
        self.url_entry.delete(0,END)
        self.target_name_entry.delete(0,END)
        self.target_type_dropdown
        self.cooldown_entry.delete(0,END)
        
        for i in range(len(self.troop_entries)):
            self.troop_entries[i].delete(0,END)
            self.troop_entries[i].insert(END,"0")
            
    def update_target_list(self,event=None):
        self.list_box.delete(0,END)
        village = self.village_dropdown.get()
        if village == "":
            # villages = TRAVIAN.get_all_villages()
            self.list_box.insert(END,"")
            return

        targets = TRAVIAN.get_targets(village)
        for target in targets:
            city_coordinates = TRAVIAN.get_coordinates(village)
            target_coordinates = target["coordinates"]
            distance = math.sqrt((target_coordinates[0]-city_coordinates[0])**2+(target_coordinates[1]-city_coordinates[1])**2)
            text = f"{village} - {target['target_name']} {target['coordinates']} - {distance:.1f}"
            self.list_box.insert(END, text)
        self.list_box.insert(END,"")
      
    def add_target(self):
        village_from = self.village_dropdown.get()
        target_name = self.target_name_entry.get()
        target_type = self.target_type_dropdown.get().lower()
        cooldown = int(self.cooldown_entry.get())
        target_url = self.url_entry.get()
        troops = {
            'Legionnaire': int(self.troop_entries[0].get()),
            'Praetorian': int(self.troop_entries[1].get()),
            'Imperian': int(self.troop_entries[2].get()),
            'Equites Legati': int(self.troop_entries[3].get()),
            'Equites Imperatoris': int(self.troop_entries[4].get()),
            'Equites Caesaris': int(self.troop_entries[5].get()),
            'Battering ram': int(self.troop_entries[6].get()),
            'Fire Catapult': int(self.troop_entries[7].get()),
            'Senator': int(self.troop_entries[8].get()),
            'Settler': int(self.troop_entries[9].get()),
            'Hero': int(self.troop_entries[10].get()),
        }
        
        TRAVIAN.add_target(village_from,target_url,target_name,target_type,troops,cooldown)
        self.update_target_list(None)
        self.empty_form()
        
    def delete_target(self):
        if self.list_box.get(ANCHOR) == "":
            return
        current_selection = self.list_box.curselection()[0]
        village_from = self.village_dropdown.get()
        TRAVIAN.delete_target_by_idx(village_from, current_selection)
        self.update_target_list()

class TradeRouteManagerUI:
    def __init__(self) -> None:
        # Atributes

        # Window
        self.root = Toplevel()
        self.root.title("Manage Trade Routes")
        self.root.config(
            padx=10,
            pady=10,
            highlightthickness=0
        )
        
        # Trade Route List
        self.list_box = Listbox(self.root,
                                height=10,
                                width=40,
                                selectmode="SINGLE")
        self.list_box.grid(
            padx=0,
            pady=0,
            column=0,
            row=0,
            rowspan=7,
            sticky=W+E+N+S
        )
        self.listbox_scrollbar = Scrollbar(self.root)
        self.listbox_scrollbar.grid(column=1,row=0, rowspan=7,sticky=W+E+N+S,padx=(0,20))
        self.list_box.config(yscrollcommand = self.listbox_scrollbar.set)
        self.listbox_scrollbar.config(command = self.list_box.yview)
        self.list_box.bind("<<ListboxSelect>>",self.root.destroy)
        
        # Permanent Buttons
        self.village_label = Label(
            self.root,
            text="Select Village:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=20
        )
        self.village_label.grid(column= 2, row=0, padx=0,sticky=W+E+N+S)

        village_list = TRAVIAN.get_all_villages()
        self.village_dropdown = ttk.Combobox(self.root,values=village_list)
        self.village_dropdown.grid(column=2,row=1,sticky=W+E+N+S)
        self.village_dropdown.bind("<<ComboboxSelected>>",self.update_trade_route_list)
        
        
        self.add_route_btn = Button(
            self.root,
            text='Add/Edit Trade Route', 
            width=13,
            height=2,
            command=self.add_new_route
        )
        self.add_route_btn.grid(column=2,row=3,rowspan=2,padx=20, sticky=W+E+N+S)
        
        self.delete_route_btn = Button(
            self.root,
            text='Delete Trade Route', 
            width=13,
            height=2,
            command=self.root.destroy
        )
        self.delete_route_btn.grid(column=2,row=5,rowspan=2,padx=20, sticky=W+E+N+S)
        
        
        # Form
        self.x_label = Label(
            self.root,
            text="X", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=5
        )
        self.x_label.grid(column=3,row=1, padx=5, sticky=W+E+N+S)
        
        self.x_entry = Entry(
            self.root,
            width=5,
            justify="center"
        )
        self.x_entry.grid(column=3,row=2, padx=5,sticky=W+E+N+S)
        
        self.y_label = Label(
            self.root,
            text="Y:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=5
        )
        self.y_label.grid(column=4,row=1, padx=5, sticky=W+E+N+S)
        
        self.y_entry = Entry(
            self.root,
            width=5,
            justify="center"
        )
        self.y_entry.grid(column=4,row=2, padx=5,sticky=W+E+N+S)
        
        self.cooldown_label = Label(
            self.root,
            text="Cooldown:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=10
        )
        self.cooldown_label.grid(column=3,row=4, columnspan=2, padx=5, sticky=W+E+N+S)
        
        self.cooldown_entry = Entry(
            self.root,
            width=5,
            justify="center"
        )
        self.cooldown_entry.grid(column=3,row=5, columnspan=2, padx=5,sticky=W+E+N+S)
        
        self.lumber_label = Label(
            self.root,
            text="Lumber:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=10
        )
        self.lumber_label.grid(column=5,row=0, padx=5, sticky=W+E+N+S)
        
        self.lumber_entry = Entry(
            self.root,
            width=10,
            justify="center"
        )
        self.lumber_entry.grid(column=6,row=0,sticky=W+E+N+S)
        
        self.clay_label = Label(
            self.root,
            text="Clay:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=10
        )
        self.clay_label.grid(column=5,row=2, padx=5, sticky=W+E+N+S)
        
        self.clay_entry = Entry(
            self.root,
            width=10,
            justify="center"
        )
        self.clay_entry.grid(column=6,row=2,sticky=W+E+N+S)
        
        self.iron_label = Label(
            self.root,
            text="Iron:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=10
        )
        self.iron_label.grid(column=5,row=4, padx=5, sticky=W+E+N+S)
        
        self.iron_entry = Entry(
            self.root,
            width=10,
            justify="center"
        )
        self.iron_entry.grid(column=6,row=4,sticky=W+E+N+S)
        
        self.crop_label = Label(
            self.root,
            text="Crop:", 
            fg="Black",
            font=("Arial",10,"normal"),
            justify= "center",
            width=10
        )
        self.crop_label.grid(column=5,row=6, padx=5, sticky=W+E+N+S)
        
        self.crop_entry = Entry(
            self.root,
            width=10,
            justify="center"
        )
        self.crop_entry.grid(column=6,row=6,sticky=W+E+N+S)
        
        for row in range(8):
           self.root.rowconfigure(row,minsize=20)
        
    def update_trade_route_list(self,event=None):
        self.list_box.delete(0,END)
        village = self.village_dropdown.get()
        if village == "":
            self.list_box.insert(END,"")
            return

        trade_routes = TRAVIAN.get_routes(village)
        for route in trade_routes:
            text = f"{village} -> {tuple(route['coordinates'])}"
            self.list_box.insert(END, text)
        self.list_box.insert(END,"")
        
    def add_new_route(self):
        city_from = self.village_dropdown.get()
        coordinates = [int(self.x_entry.get()),int(self.y_entry.get())]
        cooldown = int(self.cooldown_entry.get())
        resources = {
            "Lumber": int(self.lumber_entry.get()),
            "Clay": int(self.clay_entry.get()),
            "Iron": int(self.iron_entry.get()),
            "Crop": int(self.crop_entry.get()),
        }
        
        TRAVIAN.add_trade_route(city_from, coordinates, resources, cooldown)
        self.update_trade_route_list()
    
                    
if __name__ == "__main__":
    TRAVIAN = None
    TRAVIAN = Travian()
    ui = MainWindow()
    TRAVIAN.driver.quit()
    