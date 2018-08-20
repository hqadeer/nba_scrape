import os
import errno
import helpers
import csv
import time
import sqlite3

class Player:

    def __init__(self, id, type="trad"):

        self.id = id
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        value = cursor.execute('''SELECT count(*) FROM sqlite_master WHERE
            type='table' AND name = %s''' % str(id)).fetchone()[0]
        if value != 0:
            return
        url = "".join(["http://stats.nba.com/player/", str(id), '/career'])
        pages = helpers.get_player_trad(url)
        helpers.scrape_player_trad(pages[0], id, False)
        helpers.scrape_player_trad(pages[1], id, True)


    def get_stat(self, year='career', stat=None, playoffs=False):
        if playoffs == False:
            if stat is None:
                try:
                    value = self.season[year]
                except KeyError:
                    return None
            else:
                try:
                    value = float(self.season[year][str(stat).upper()])
                except KeyError:
                    return None
        elif playoffs == True:
            if stat is None:
                try:
                    value = self.playoffs[year]
                except KeyError:
                    return None
            else:
                try:
                    value = float(self.playoffs[year][str(stat).upper()])
                except KeyError:
                    return None
        if value not in (None, ""):
            return value




if __name__ == "__main__":
    lbj = Player(2544)
