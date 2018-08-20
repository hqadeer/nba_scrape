from helpers import get_players
from entities import Player
import os
import csv
import helpers
import sqlite3

class NBA:


    def __init__(self):
        #helpers.setup()
        file_name = "data.db"
        if os.path.isfile(file_name):
            if not os.path.isdir(os.path.dirname(file_name)):
                try:
                    os.makedirs(os.path.dirname(file_name))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            page = get_players('http://stats.nba.com/players/list/?Historic=Y')
            db = sqlite3.connect('data.db')
            cursor = db.cursor()
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

    def get_player(self, name):
        return Player(self.players[name])


    def load_all_players(self):
        print("Starting")
        for key in self.players:
            print(key)
            try:
                temp = Player(self.players[key])
            except NoSuchElementException:
                time.sleep(2)
                temp = Player(self.players[key])


if __name__ == "__main__":
    scraper = NBA()
    #temp = Player(scraper.players['dwight howard'])
