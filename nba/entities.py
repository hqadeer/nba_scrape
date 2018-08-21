import os
import errno
import helpers
import csv
import time
import sqlite3

class Player:

    def __init__(self, id, advanced=False):

        self.id = id
        self.table_name = 'p' + str(id)
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        value = cursor.execute('''SELECT count(*) FROM sqlite_master WHERE
            type='table' AND name = %s''' % ''.join(['"', self.table_name,
            '"'])).fetchone()[0]
        db.close()
        if value == 0:
            url = "".join(["http://stats.nba.com/player/", str(id), '/career'])
            pages = helpers.get_player_trad(url)
            helpers.scrape_player_trad(pages[0], id, False)
            helpers.scrape_player_trad(pages[1], id, True)
        self.season_stats = {}
        self.playoffs_stats = {}

    def get_stat(self, stat, year='career', playoffs=False):
        if playoffs == False:
            store = self.season_stats
        else:
            store = self.playoffs_stats
        stat = stat.upper()
        year = year.upper()
        if "3" in stat:
            stat = stat.replace("3", "three")
        if "%" in stat:
            stat = stat.replace("%", "percent")
        if year in store and stat in store[year]:
            return store[year][stat]
        else:
            db = sqlite3.connect('data.db')
            cursor = db.cursor()
            cursor.execute('''SELECT %s FROM %s WHERE Season = %s''' %
                (str(stat), self.table_name, ''.join(['"', str(year),
                '"'])))
            value = cursor.fetchone()
            db.close()
            if value is None:
                raise AttributeError("Invalid query: %s, %s" % (stat, year))
            if year in store:
                store[year][stat] = value[0]
            else:
                temp = {stat: value[0]}
                store[year] = temp
            return value[0]

    def get_all_stats(self, mode="both"):

        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        if mode == "both":
            cursor.execute('''SELECT * FROM %s''' % self.table_name)
        elif mode == "playoffs":
            cursor.execute('''SELECT * FROM %s WHERE playoffs = 1'''
                % self.table_name)
        elif mode == "season":
            cursor.execute('''SELECT * FROM %s WHERE playoffs = 0'''
                % self.table_name)
        else:
            raise ValueError("Invalid argument passed to 'mode'")
        return cursor.fetchall()


if __name__ == "__main__":
    lbj = Player(2544)
    lbj.get_stat('pts', '2008-09')
