# --- Imports --- #
import requests
from bs4 import BeautifulSoup

# --- Global Variables --- #
URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
ROOT = "Day 041 - 050/Day 045 - Web Scrapping/"

# --- Functions --- #
def get_soup(url:str) -> BeautifulSoup:
    response = requests.get(url)
    website = response.text
    return BeautifulSoup(website,"html.parser")

# --- Program --- #
soup = get_soup(URL)
titles_obj = soup.select("h3")
titles_obj.reverse()

titles_text = [title.getText() for title in titles_obj]

with open(ROOT+"movies.txt","w+", encoding="utf-8") as file:
    for i in range(len(titles_text)):
        file.write(titles_text[i]+"\n")