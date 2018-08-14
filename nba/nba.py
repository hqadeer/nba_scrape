from selenium import webdriver
from bs4 import BeautifulSoup

class NBA:


    def __init__(self):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = webdriver.Chrome(chrome_options=options)
        driver.get('http://stats.nba.com/players/list/?Historic=Y')

        soup = BeautifulSoup(driver.page_source, features='lxml')
        driver.close()

        self.players = {}
        for player in soup.find_all("li", class_="players-list__name"):
            id = int(str(player.a['href']).split('/')[2].split('/')[0])
            name_comps = player.a.string.split(', ')
            if len(name_comps) == 2:
                name = (' '.join([name_comps[1], name_comps[0]])).lower()
            else:
                name = name_comps[0].lower()
            if id == 2544:
                print (name)
            self.players[name] = id

print (players['lebron james'])
print (players['kobe bryant'])
