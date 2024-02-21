# --- Imports --- #
from item_manager import ItemManager
from add_items import add_items
from generic_functions import send_mail
import os

# --- Global Variables --- #
PRODUCT_URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
ROOT = "Day 041 - 050/Day 047 - Amazon Price Tracker/"
# --- Functions --- #


# --- Program --- #
# 1 - Create/add products to a list. Each item should contain: common name, url, prices, reference price. This should be a separate file.
try:
    with open(f"{ROOT}product_list.json")as file:
        pass
except FileNotFoundError:
    add_items()
    
item_manager = ItemManager()


# 2 - Update the price for all products
item_list = item_manager.get_items()
items_to_notify = []
for item in item_list:
    price = item_manager.check_price(item)
    if price < item_manager.get_reference_price(item):
        items_to_notify.append(item)
             
# 3 - Send e-mail with items to notify.
recipients = [os.environ.get("TO_TEST_EMAIL")]
if len(items_to_notify) > 0:
    if len(items_to_notify) > 1:
        message_body = f"{len(items_to_notify)} items you are tracking are at a low price!!!\n\n"
        message_title = message_body
    if len(items_to_notify) == 1:
        message_body = f"1 item you are tracking is at a low price!!!\n\n"
        message_title = message_body
    for item in items_to_notify:
        message_body += f"{item} is now at {item_manager.get_item_current_price(item)}!!!\nLink: {item_manager.get_item_url(item)}\n\n"
    send_mail(
        subject= message_title,
        body= message_body,
        recipients= recipients
        )
item_manager.save_data()