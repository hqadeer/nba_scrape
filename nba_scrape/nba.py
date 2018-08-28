from nba_scrape.helpers import get_players
from nba_scrape.entities import Player
import os
import sys
import sqlite3
import time

class NBA:

    '''Core class by which NBA stats can be accessed.'''

    def __init__(self, update=False):

        '''Initializes list of NBA players to database if not already present

        update (bool) -- If true, init will re-initialize the list of players
        even if a current list of players exists on the database. This allows
        user to update the list for new players.
        '''

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

        '''Returns a Player object based on the given name.

        If the player is not found in the database's list of players, an
        AttributeError is raised.

        name (str) -- name of the player desired, case-insensitive.
        '''

        name = name.lower()
        if name in self.players:
            id = self.players[name]
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

        '''Returns a player object based on the given ID.

        Raises an AttributeError if the provided ID does not correspond to a
        known player.

        id (int) -- ID of the player desired.
        '''

        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM players WHERE id = %d''' % int(id))
        if cursor.fetchone() is None:
            raise AttributeError("No player with id: %s" % str(id))
        return Player(id)

    def load_all_players(self):

        '''Loads all NBA players to local database.

        WARNING: This takes multiple hours to complete and will use a non-
        negligible amount of disk storage.
        '''

        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM players''')
        list = cursor.fetchall()
        db.close()
        for id in list:
            print(id[0])
            temp = Player(id[1])


if __name__ == "__main__":

    league = NBA()
    begin = time.time()
    lebron = league.get_player_by_id(2544)
    print(lebron.get_stat('TS%', '2012-13', playoffs=True))
    print(lebron.get_stats(['FT%', '3P%'], '2015-18', mode="playoffs"))
    print(lebron.get_all_stats(mode="playoffs"))
    print(time.time() - begin)
