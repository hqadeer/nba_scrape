import os
import traceback
import sqlite3
import copy
from nba_scrape.nba_exceptions import InvalidStatError
import nba_scrape.helpers as helpers
import nba_scrape.constants as constants

class Player:
    '''Class representing an NBA player.'''


    def __init__(self, id):
        ''' Build player table if it doesn't already exist

            id (int) -- player ID number
        '''

        self.id = int(id)
        db = sqlite3.connect('data.db')
        cursor = db.cursor()

        try:
            value = cursor.execute('''SELECT count(*) FROM tradstats WHERE
                ID=?''', (self.id,)).fetchone()[0]
        except (sqlite3.OperationalError, IndexError) as exc:
            value = 0

        db.close()
        if value == 0:
            url = "".join(["http://stats.nba.com/player/", str(self.id),
                '/career'])
            pages = helpers.get_player_trad(url)
            if pages[0] is not None:
                helpers.scrape_player_trad(pages[0], self.id, False)
            if pages[1] is not None:
                helpers.scrape_player_trad(pages[1], self.id, True)
            elif pages[0] is None:
                helpers.create_empty_row(self.id)
        self.season_stats = {}
        self.playoffs_stats = {}

    def get_stat(self, stat, year='career', playoffs=False):
        '''Return instance player's specified stat for the specified year.

        Format input stat to account for capitalization.
        Compute TS% by recursively calling method for points, FGA, and FTA.
        For players who were traded mid-season, return stats from the whole
        season.
        Raise InvalidStatError if stat/year do not exist.

        stat (str) -- desired statistic; FGA, FTM, FG%, 3PM, PTS, AST, etc.
        year (str) -- desired season (i.e. '2003-04'). Overall stats
                      (season='career') given if no season specified.
        playoffs (bool) -- True = playoffs stats, False = season stats
        '''

        if not playoffs:
            store = self.season_stats
            pvalue = 0
        else:
            store = self.playoffs_stats
            pvalue = 1
        stat = stat.upper()
        if stat in constants.unsupported_stats:
            raise InvalidStatError("No support yet for %s queries" % stat)
        if stat not in constants.supported_stats:
            raise InvalidStatError("Invalid stat query: %s" % stat)
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
                if playoffs:
                    send_mode = "playoffs"
                else:
                    send_mode = "season"
                points, fga, fta = (self.get_stats(['PTS', 'FGA', 'FTA'], year,
                                    mode=send_mode))[0]
                value = [round(points / (2 * (fga + 0.44 * fta)), 3)]
            else:
                db = sqlite3.connect('data.db')
                cursor = db.cursor()
                try:
                    cursor.execute('''SELECT %s FROM tradstats WHERE ID=:id
                                   AND PLAYOFFS=:flip AND Season=:year ORDER
                                   BY GP DESC''' % str(stat), {"id": self.id,
                                   "flip": pvalue, "year": year})
                    value = cursor.fetchone()
                except sqlite3.OperationalError:
                    raise sqlite3.OperationalError("An error occurred during "
                                                   + "database retrieval")
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
        '''Return a list of tuples of player stats.
        More efficient than repeatedly calling get_stat

        Can return a range of stats over a range of seasons.
        For players who were traded mid-season, return both total stats and
        stats for each team.

        stats (list) -- stats desired. I.e. ['PTS', 'AST', 'REB']
        year_range (str) -- seasons desired. '2004-10' would return stats from
                            the 2004-05 season to the 2009-10 season. Range can
                            also be 'career', returning overall stats, or None,
                            returning stats from all seasons (and overall
                            averages).
        mode (str) -- must be 'season', 'playoffs', or 'both'.

        Stats are returned in the order specified, from least to most recent
        season specified. "Career" is counted as the most recent season.
        '''
        pvalues = []
        if mode.lower() == "season":
            pvalue = 0
        elif mode.lower() == "playoffs":
            pvalue = 1
        elif mode.lower() != "both":
            raise ValueError("Mode must be 'season', 'playoffs', or 'both'.")

        seasons = self.get_year_range(year_range)

        for i, stat in enumerate(stats):
            if stat.upper() not in constants.supported_stats:
                raise InvalidStatError("Invalid stat: %s" % stat)
            if stat.upper() == 'TS%':
                if mode == 'both':
                    old_stats = copy.deepcopy(stats)
                    return (
                        self.get_stats(stats, year_range, mode='season') +
                        self.get_stats(old_stats, year_range, mode='playoffs')
                    )
                stats.remove(stat)
                tuples = zip(seasons, self.get_stats(stats, year_range,
                             mode))
                return [pair[:i] + (self.get_stat('TS%', season,
                        playoffs=pvalue),) + pair[i:] for season, pair in
                        tuples]

        for i, stat in enumerate(stats):
            stats[i] = ''.join(['"', stat.upper(), '"'])
            if "%" in stats[i]:
                stats[i] = stats[i].replace("%", "percent")
            if "3" in stats[i]:
                stats[i] = stats[i].replace("3", "three")
            helpers.scrub(stats[i])

        for i, season in enumerate(seasons):
            seasons[i] = ''.join(['"', season, '"'])

        if len(stats) < 1:
            raise ValueError("Please request at least one stat.")

        stat_hold = ', '.join('?' * len(stats))
        db = sqlite3.connect('data.db')
        cursor = db.cursor()

        try:
            if seasons is None:
                if mode.lower() == "both":
                    cursor.execute('''SELECT %s FROM tradstats WHERE ID=?
                                   ORDER BY PLAYOFFS, Season''' %
                                   ', '.join(stats), (self.id,))
                else:
                    cursor.execute('''SELECT %s FROM tradstats WHERE ID=?
                                   AND PLAYOFFS=? ORDER BY Season''' %
                                   ', '.join(stats), (self.id, pvalue))
            else:
                season_hold = ', '.join('?' * len(seasons))
                if mode.lower() == "both":
                    cursor.execute('''SELECT %s FROM tradstats WHERE ID=?
                                   AND Season IN (%s) ORDER BY PLAYOFFS,
                                   Season''' % (', '.join(stats),
                                   ', '.join(seasons)), (self.id,))
                else:
                    cursor.execute('''SELECT %s FROM tradstats WHERE ID=? AND
                                   PLAYOFFS=? AND Season IN (%s) ORDER BY
                                   Season''' % (', '.join(stats),
                                   ', '.join(seasons)), (self.id, pvalue))

            temp = cursor.fetchall()
        except sqlite3.OperationalError as exc:
            traceback.print_exc()
            raise InvalidStatError("Error occurred during database retrieval.")
        finally:
            db.close()

        return temp

    def get_year_range(self, year_range):
        '''Takes in a range of years and returns the years in that range.

        year_range (string) -- Range of years, like '2006-10' or '1998-04'.
                               Can also be 'Career' for overall stats or None
                               for all stats.
        '''
        if year_range is None:
            return None
        if (year_range.upper() != "CAREER" and
                (len(year_range) != 7 or "-" not in year_range)):
            raise ValueError("Invalid year range provided: %s" % year_range)
        if year_range.upper() != "CAREER":
            helpers.scrub(year_range)
            years = year_range.split('-')
            begin_year = years[0]
            if int(begin_year[2:4]) < int(years[1]):
                end_year = int(begin_year[0:2] + years[1])
            else:
                end_year = int(str(int(begin_year[0:2]) + 1) + years[1])
            seasons = []
            while int(begin_year) < int(end_year):
                seasons.append('-'.join([begin_year,
                               str(int(begin_year)+1)[2:4]]))
                begin_year = str(int(begin_year) + 1)
        else:
            seasons = ['"CAREER"']
        return seasons

    def get_all_stats(self, mode="both"):
        '''Query database to return list of tuples of all player stats.

        mode (str) -- 'season', 'playoffs', or 'both'. Determines what type of
                      stats are returned.
        '''

        try:
            db = sqlite3.connect('data.db')
            cursor = db.cursor()
            if mode.lower() == "both":
                cursor.execute('''SELECT * FROM tradstats WHERE id=? ORDER BY
                    playoffs, Season''', (self.id,))
            elif mode.lower() == "playoffs":
                cursor.execute('''SELECT * FROM tradstats WHERE id=? AND
                    playoffs = 1 ORDER BY Season''', (self.id,))
            elif mode.lower() == "season":
                cursor.execute('''SELECT * FROM tradstats WHERE id=? AND
                playoffs = 0 ORDER BY Season''', (self.id,))
            else:
                raise ValueError("Invalid argument passed to 'mode'")

            stats = cursor.fetchall()

        finally:
            db.close()

        return stats

if __name__ == "__main__":

    lbj = Player(2544)
