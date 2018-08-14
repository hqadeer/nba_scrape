from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(chrome_options=options)
driver.get('http://stats.nba.com/players/list/?Historic=Y')

soup = BeautifulSoup(driver.page_source, features='lxml')
driver.close()

players = soup.find_all("li", class_="players-list__name", limit=2)

with open('new.txt', 'w') as f:
    for player in players:
        f.write(str(player['a']))
