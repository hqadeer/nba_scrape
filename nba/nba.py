from helpers import get_players
from entities import Player
import os
import csv
import helpers
import sqlite3

class NBA:


    def __init__(self):

        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        value = cursor.execute('''SELECT count(*) FROM sqlite_master WHERE
            type='table' AND name = "players"''').fetchone()[0]
        if value != 0:
            return
        page = get_players('http://stats.nba.com/players/list/?Historic=Y')
        names = []
        for player in page.find_all("li", class_="players-list__name"):
            id = str(player.a['href']).split('/')[2].split('/')[0]
            name_comps = player.a.string.split(', ')
            if len(name_comps) == 2:
                name = (' '.join([name_comps[1], name_comps[0]])).lower()
            else:
                name = name_comps[0].lower()
            names.append((name, int(id)))

        cursor.execute('''CREATE TABLE players(name TEXT, id INTEGER)''')
        cursor.executemany('''INSERT INTO players (name, id) values (?, ?)''',
            names)
        db.commit()

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
