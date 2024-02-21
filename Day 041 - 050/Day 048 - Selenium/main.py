# The following bot was created as a learning exercise for the use of Selenium. It is not meant to be used for any competitive advantage.

# --- Imports --- #
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
import os

# --- Global Variables --- #
URL = "https://ts1.x1.international.travian.com/"

# --- Functions --- #

# --- Program --- #
# Start Browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

# Login
account_name_input = driver.find_element(By.CSS_SELECTOR,".account input")
password_input = driver.find_element(By.CSS_SELECTOR,".pass input")
login_button = driver.find_element(By.CSS_SELECTOR,".loginButtonRow button")

account_name_input.send_keys(os.environ.get("TRAVIAN_ACCOUNT"))
password_input.send_keys(os.environ.get("TRAVIAN_PASSWORD"))
login_button.click()
    
# pprint()

#driver.close() # Closes a single tab.
#driver.quit()