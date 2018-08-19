import os
import errno
import helpers
import csv
import time

class Player:


    def __init__(self, id):

        self.season_filename = "".join(['nba/data/players/season/',
            str(id), '.csv'])
        self.playoffs_filename = "".join(['nba/data/players/playoffs/',
            str(id), '.csv'])
        url = "".join(["http://stats.nba.com/player/", str(id), '/career'])
        files = [self.season_filename, self.playoffs_filename]
        for file in files:
            if not os.path.isdir(os.path.dirname(file)):
                try:
                    os.makedirs(os.path.dirname(file))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
        if (not os.path.isfile(self.season_filename) and
                not os.path.isfile(self.playoffs_filename)):
            pages = helpers.get_player(url)
            helpers.scrape_player(pages[0], self.season_filename)
            helpers.scrape_player(pages[1], self.playoffs_filename)
        elif not os.path.isfile(self.playoffs_filename):
            pages = helper.get_player(url, mode="playoffs")
            helpers.scrape_player(pages[0], self.playoffs_filename)
        elif not os.path.isfile(self.season_filename):
            pages = helper.get_player(url, mode="season")
            helpers.scrape_player(pages[0], self.season_filename)
        self.season = {}
        self.playoffs = {}
        with open(self.season_filename, newline='') as f:
            season_reader = csv.DictReader(f)
            for row in season_reader:
                row['TS%'] = float(row['PTS']) / (2 *
                    (float(row['FGA']) + 0.44 * float(row['FTA'])))
                self.season[row['Season']] = row
        self.season['career'] = self.season.pop('Overall: ')
        with open(self.playoffs_filename, newline='') as f:
            playoffs_reader = csv.DictReader(f)
            for row in playoffs_reader:
                row['TS%'] = float(row['PTS']) / (2 *
                    (float(row['FGA']) + 0.44 * float(row['FTA'])))
                self.playoffs[row['Season']] = row
        self.playoffs['career'] = self.playoffs.pop('Overall: ')

    def get_stat(self, year, stat=None, playoffs=False):
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
    lbj = Player(78049)
    print(lbj.get_stat('1956-57', 'ts%'))
