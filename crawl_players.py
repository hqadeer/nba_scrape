import requests
from bs4 import BeautifulSoup


url = ('http://stats.nba.com/players/list/')
r = requests.get(url)
soup = BeautifulSoup(r.content)

with open('new.txt', 'w') as f:
    f.write(soup.prettify())
