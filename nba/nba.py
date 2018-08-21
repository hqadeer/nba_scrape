from helpers import get_players
from entities import Player
import os
import sys
import helpers
import sqlite3
import time

class NBA:


    def __init__(self, update=False):

        self.players = {}
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        if not update:
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
        db.close()

    def get_player(self, name):
        if name.lower() in self.players:
            id = self.players[name.lower()]
        else:
            db = sqlite3.connect('data.db')
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM players WHERE name = %s'''
                % ''.join(['"', name, '"']))
            pair = cursor.fetchone()
            if pair is None:
                raise AttributeError("No player with name: %s" % name)
            db.close()
            self.players[pair[0]] = pair[1]
            id = pair[1]
        return Player(id)

    def get_player_by_id(self, id):
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM players WHERE id = %d''' % int(id))
        if cursor.fetchone() is None:
            raise AttributeError("No player with id: %s" % str(id))
        return Player(id)


if __name__ == "__main__":
    begin = time.time()
    league = NBA()
    lebron = league.get_player('bill russell')
    print (lebron.get_stat('TS%', '1966-97'))
    print(time.time() - begin)
    #temp = Player(scraper.players['dwight howard'])
