from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint

URL = "https://www.python.org/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

#input("Press ENTER to continue.")
news = {}
for i in range(5):
    time = driver.find_element(By.XPATH, value=f"/html/body/div/div[3]/div/section/div[2]/div[2]/div/ul/li[{i+1}]/time")
    title = driver.find_element(By.XPATH, value=f"/html/body/div/div[3]/div/section/div[2]/div[2]/div/ul/li[{i+1}]/a")
    news[i]={
        'time': time.text,
        'title': title.text,
    }
    
pprint(news)
#driver.close() # Closes a single tab.
driver.quit()