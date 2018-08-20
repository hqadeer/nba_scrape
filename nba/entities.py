import os
import errno
import helpers
import csv
import time
import sqlite3

class Player:

    def __init__(self, id, mode="both", type="trad"):

        self.id = id
        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        value = cursor.execute('''SELECT count(*) FROM sqlite_master WHERE
            type='table' AND name = %s''' % str(id)).fetchone()[0]
        if value != 0:
            return
        url = "".join(["http://stats.nba.com/player/", str(id), '/career'])
        pages = helpers.get_player_trad(url)
        if mode in ["both", "season"]:
            helpers.scrape_player_trad(pages[0], id, False)
        if mode in ["both", "playoffs"]:
            helpers.scrape_player_trad(pages[1], id, True)
        self.season = {}
        self.playoffs = {}
        with open(self.season_filename, newline='') as f:
            season_reader = csv.DictReader(f)
            for row in season_reader:
                row['TS%'] = float(row['PTS']) / (.02 *
                    (float(row['FGA']) + 0.44 * float(row['FTA'])))
                self.season[row['Season']] = row
        self.season['career'] = self.season.pop('Overall: ')
        with open(self.playoffs_filename, newline='') as f:
            playoffs_reader = csv.DictReader(f)
            for row in playoffs_reader:
                row['TS%'] = float(row['PTS']) / (.02 *
                    (float(row['FGA']) + 0.44 * float(row['FTA'])))
                self.playoffs[row['Season']] = row
        self.playoffs['career'] = self.playoffs.pop('Overall: ')


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
