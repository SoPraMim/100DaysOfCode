from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint

URL = "https://en.wikipedia.org/wiki/Main_Page"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

#input("Press ENTER to continue.")
n_articles = driver.find_element(By.XPATH, value="/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/div[1]/div/div[3]/a[1]")
n_articles = int(n_articles.text.replace(",",""))
    
pprint(n_articles)

#driver.close() # Closes a single tab.
driver.quit()