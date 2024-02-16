from item_manager import ItemManager
from generic_functions import cls

def add_items():
    cls()
    item_manager = ItemManager()
    item_manager.add_item()
    item_manager.save_data()

if __name__ == "__main__":
    add_items()