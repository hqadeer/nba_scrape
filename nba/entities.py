import os
import errno
import helpers
import csv
import time
import sqlite3

class Player:

    def __init__(self, id, advanced=False):

        self.id = id
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        value = cursor.execute('''SELECT count(*) FROM sqlite_master WHERE
            type='table' AND name = %s''' % str(id)).fetchone()[0]
        db.close()
        if value == 0:
            url = "".join(["http://stats.nba.com/player/", str(id), '/career'])
            pages = helpers.get_player_trad(url)
            helpers.scrape_player_trad(pages[0], id, False)
            helpers.scrape_player_trad(pages[1], id, True)
        season_stats = {}
        playoffs_stats = {}

    def get_stat(self, stat, year='career', playoffs=False):
        if playoffs = False:
            store = self.season_stats
        else:
            store = self.playoffs_stats
        if "3" in stat:
            stat = stat.replace("3", "three")
        if "%" in stat:
            stat = stat.replace("%", "percent")
        if year in store and stat in store[year]:
            return store[year][stat]
        else:
            db = sqlite3.connect('data.db')
            cursor = db.cursor()
            cursor.execute('''SELECT %s FROM %s WHERE year = %s''' %
                (stat, ''.join(['p', str(id)]), year)
            value = cursor.fetchone()
            db.close()
            if value is None:
                raise AttributeError("Invalid query: %s, %s" % (stat, year))
            if year in store:
                store[year][stat] = value
            else:
                temp = {stat: value}
                store[year] = temp







if __name__ == "__main__":
    lbj = Player(2544)
