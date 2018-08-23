import os
import errno
import helpers
import csv
import time
import sqlite3
from nba_exceptions import InvalidStatError
import time

class Player:

    # Class representing an NBA player.

    def __init__(self, id, advanced=False):

        # If player has not been loaded before, scrape season and playoffs data
        # to database table. Initialize two empty dicts.

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
            if pages[0] is not None:
                helpers.scrape_player_trad(pages[0], id, False)
            if pages[1] is not None:
                helpers.scrape_player_trad(pages[1], id, True)
            elif pages[0] is None:
                helpers.create_empty_table(id)
        self.season_stats = {}
        self.playoffs_stats = {}

    def get_stat(self, stat, year='career', playoffs=False):

        # Return instance player's specified stat for the specified year.
        # Format input stat to account for capitalization.
        # Compute TS% by recursively calling method for points, FGA, and FTA.
        # Raise InvalidStatError if stat/year do not exist.

        if playoffs == False:
            store = self.season_stats
            pvalue = 0
        else:
            store = self.playoffs_stats
            pvalue = 1
        stat = stat.upper()
        year = year.upper()
        helpers.scrub(year)
        if "3" in stat:
            stat = stat.replace("3", "three")
        if "%" in stat:
            stat = stat.replace("%", "percent")
        if year in store and stat in store[year]:
            return store[year][stat]
        else:
            helpers.scrub(stat)
            if stat == "TSpercent":
                if playoffs == False:
                    send_mode = "season"
                else:
                    send_mode = "playoffs"
                points, field_goals_attempted, free_throws_attempted = (
                    self.get_stats(['PTS', 'FGA', 'FTA'], year,
                    mode=send_mode))[0]
                value = (points / (2*(field_goals_attempted +
                    0.44 * free_throws_attempted)), )
            else:
                if ';' in stat or ';' in year:
                    raise ValueError("No semicolons allowed in inputs.")
                db = sqlite3.connect('data.db')
                cursor = db.cursor()
                try:
                    cursor.execute('''SELECT ? FROM %s WHERE Season=? AND
                        PLAYOFFS = %d''' % self.table_name, (str(stat),
                        ''.join(['"', str(year), '"']), pvalue))
                    value = cursor.fetchone()
                except sqlite3.OperationalError:
                    raise InvalidStatError("%s does not exist for player %d"
                        % (stat, self.id))
                finally:
                    db.close()
            if value is None:
                return None
            if year in store:
                store[year][stat] = value[0]
            else:
                temp = {stat: value[0]}
                store[year] = temp
            return value[0]

    def get_stats(self, stats, year_range=None, mode="season"):

        # Return a list of tuples for player stats from a specified range of
        # seasons. Year ranges should be in the format YYYY-YY; 2004-10 refers
        # to the 2004-05 season (2005 playoffs) through the 2009-10 season
        # (2010 playoffs).

        # To do: Add support for TS% queries.

        pvalues = []
        if mode.lower() == "season":
            pvalue = 0
        elif mode.lower() == "playoffs":
            pvalue = 1
        elif mode.lower() != "both":
            raise ValueError("Mode must be 'season', 'playoffs', or 'both'.")

        for i, stat in enumerate(stats):
            stats[i] = ''.join(['"', stat.upper(), '"'])
            if "3" in stat:
                stats[i] = stat.replace("3", "three")
            if "%" in stats[i]:
                stats[i] = stat.replace("%", "percent")
            helpers.scrub(stats)

        if "TSpercent" in stats:
            raise ValueError("Invalid stat for multi-stat queries: TS%")

        if (year_range is not None and year_range.upper() != "CAREER" and
                (len(year_range) != 7 or "-" not in year_range)):
            raise ValueError("Invalid year range provided: %s" % year_range)
        if len(stats) < 1:
            raise ValueError("Please provide at least one stat.")

        helpers.scrub(year_range)
        if year_range is not None and year_range.upper() != "CAREER":
            years = year_range.split('-')
            begin_year = years[0]
            if int(begin_year[2:4]) < int(years[1]):
                end_year = int(begin_year[0:2] + years[1])
            else:
                end_year = int(str(int(begin_year[0:2]) + 1) + years[1])
            seasons = []
            while int(begin_year) < int(end_year):
                seasons.append(''.join(['"', '-'.join([begin_year,
                str(int(begin_year)+1)[2:4]]), '"']))
                begin_year = str(int(begin_year) + 1)
        elif year_range.upper() == "CAREER":
            seasons = ['"CAREER"']

        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        try:
            if year_range is None and mode.lower() == "both":
                cursor.execute('''SELECT (%) FROM %s ORDER BY Season'''
                    % (', '.join(stats), self.table_name))
            elif year_range is None:
                cursor.execute('''SELECT %s FROM %s WHERE PLAYOFFS = %d
                    AND Season IN (%s) ORDER BY Season''' % (', '.join(stats),
                    self.table_name, pvalue, ', '.join(seasons)))
            if mode.lower() == "both":
                cursor.execute('''SELECT (%s) FROM %s WHERE Season IN (%s)
                    ORDER BY Season''' % (', '.join(stats),
                    self.table_name, ', '.join(seasons)))
            else:
                cursor.execute('''SELECT %s FROM %s WHERE PLAYOFFS = %d
                    AND Season IN (%s) ORDER BY Season''' % (', '.join(stats),
                    self.table_name, pvalue, ', '.join(seasons)))
            temp = cursor.fetchall()
        finally:
            db.close()
        return(temp)

    def get_all_stats(self, mode="both"):

        # Query database to return list of tuples of all player stats.
        # Return sesason stats, playoffs stats, or both based on specified mode.

        db = sqlite3.connect('data.db')
        cursor = db.cursor()
        if mode == "both":
            cursor.execute('''SELECT * FROM %s''' % self.table_name)
        elif mode == "playoffs":
            cursor.execute('''SELECT * FROM %s WHERE playoffs = 1 ORDER BY
                Season''' % self.table_name)
        elif mode == "season":
            cursor.execute('''SELECT * FROM %s WHERE playoffs = 0 ORDER BY
                Season''' % self.table_name)
        else:
            raise ValueError("Invalid argument passed to 'mode'")
        return cursor.fetchall()


if __name__ == "__main__":
    lbj = Player(2544)
    begin1 = time.time()
    print(lbj.get_stat('TS%', 'career', playoffs=True))
    print(lbj.get_stats(['pts', 'ast', 'reb'], '2003-04'))
    print(time.time() - begin1)
