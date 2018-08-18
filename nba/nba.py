from helpers import get_players
from entities import Player
import os
import csv
import time

class NBA:


    def __init__(self):
        file_name = "nba/data/players.csv"
        if not os.path.isfile(file_name):
            if not os.path.isdir(os.path.dirname(file_name)):
                try:
                    os.makedirs(os.path.dirname(file_name))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            page = get_players('http://stats.nba.com/players/list/?Historic=Y')
            with open(file_name, 'w', newline='') as f:
                player_writer = csv.writer(f)
                for player in page.find_all("li", class_="players-list__name"):
                    id = str(player.a['href']).split('/')[2].split('/')[0]
                    name_comps = player.a.string.split(', ')
                    if len(name_comps) == 2:
                        name = (' '.join([name_comps[1], name_comps[0]])).lower()
                    else:
                        name = name_comps[0].lower()
                    player_writer.writerow([name, id])
        self.players = {}
        with open(file_name, newline='') as f:
            player_reader = csv.reader(f)
            for row in player_reader:
                self.players[row[0]] = row[1]




    def load_all_players(self):
        print("Starting")
        for key in self.players:
            print(key)
            try:
                temp = Player(self.players[key])
            except NoSuchElementException:
                time.sleep(2)
                temp = Player(self.players[key])




    #ef get_player(self, id=None, name=None):

if __name__ == "__main__":
    scraper = NBA()
    begin = time.time()
    temp = Player(scraper.players['michael jordan'])
    print (time.time() - begin)
