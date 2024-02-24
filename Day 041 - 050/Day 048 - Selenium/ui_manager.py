# --- IMPORTS --- #
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from travian_manager import Travian

# --- GLOBAL VARIABLES ---#

ROOT = "Day 041 - 050/Day 048 - Selenium/"
# travian = Travian()


# --- USER INTERFACE --- #
class MainWindow:
    def __init__(self,travian:Travian) -> None:
        self.travian = travian
          
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


        self.root.mainloop()

    # --- COMMANDS --- #
    def __start_queue(self):
        self.start_queue_btn.configure(text = "Stop Queue", command=self.__stop_queue)
        
    def __stop_queue(self):
        self.start_queue_btn.configure(text = "Start Queue", command=self.__start_queue)
        
    def __open_queue_manager(self):
        QueueManager(self.travian)
        
class QueueManager:
    def __init__(self,travian:Travian) -> None:
        self.travian = ["test1", "test2"]
        # Window
        self.root = Tk()
        self.root.title("Manage Queue")
        self.root.config(
           
            padx=10,
            pady=10,
            highlightthickness=0
        )
        
        # Tasklist
        
        self.list_box = Listbox(self.root, height=5, width=30)
        self.list_box.grid(
            padx=20,
            pady=0,
            column=0,
            row=0,
            rowspan=6
        )
        for item in self.travian:
            self.list_box.insert(END, item)
            
        # Dropdown Menus        
        self.village_label = Label(self.root,
                              text="Select Village:", 
                              fg="Black",
                              font=("Arial",10,"normal"),
                              justify= "center",
                              width=20)
        self.village_label.grid(column= 1, row=0,padx=0,sticky=W+E+N+S)

        village_list = ["SPM 01"] # get the list of villages
        self.village_dropdown = ttk.Combobox(self.root,values=village_list)
        self.village_dropdown.grid(column=1,row=1,sticky=W+E+N+S)
        
        self.task_label = Label(self.root,
                               text="Select Task:", 
                               fg="Black",
                               font=("Arial",10,"normal"),
                               justify= "center",
                               width=20)
        self.task_label.grid(column= 1, row=2,padx=0,sticky=W+E+N+S)
        self.task_dropdown = ttk.Combobox(self.root,values=village_list)
        self.task_dropdown.grid(column=1,row=3,sticky=W+E+N+S)
        
        self.root.mainloop()
    
    
    
if __name__ == "__main__":
    UI = MainWindow(None)