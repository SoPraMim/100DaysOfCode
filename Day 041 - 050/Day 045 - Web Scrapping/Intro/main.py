from bs4 import BeautifulSoup
import requests

# with open("Day 041 - 050/Day 045 - Web Scrapping/website.html") as file:
#     content = file.read()
    
# soup = BeautifulSoup(content, "html.parser")
# print(soup.prettify())

response = requests.get("https://news.ycombinator.com/news")
website = response.text
soup = BeautifulSoup(website,"html.parser")

print(soup.select_one(".title a"))