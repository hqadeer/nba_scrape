import os
import errno
import helpers

class Player:


    def __init__(self, id):

        self.season_filename = "".join(['nba/data/players/season/',
            str(id), '.csv'])
        self.playoffs_filename = "".join(['nba/data/players/playoffs/',
            str(id), '.csv'])
        url = "".join(["http://stats.nba.com/player/", str(id), '/'])
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
            if helpers.is_active(pages[0]):
                helpers.scrape_active_player(pages[0], self.season_filename)
                helpers.scrape_active_player(pages[1], self.playoffs_filename)
            else:
                helpers.scrape_retired_player(pages[0], self.season_filename)
                helpers.scrape_retired_player(pages[1], self.playoffs_filename)
        elif not os.path.isfile(self.playoffs_filename):
            pages = helper.get_player(url, mode="playoffs")
            if helpers.is_active(pages[0]):
                helpers.scrape_active_player(pages[0], self.playoffs_filename)
            else:
                helpers.scrape_retired_player(pages[0], self.playoffs_filename)
        elif not os.path.isfile(self.season_filename):
            pages = helper.get_player(url, mode="season")
            if helpers.is_active(pages[0]):
                helpers.scrape_active_player(pages[0], self.season_filename)
            else:
                helpers.scrape_retired_player(pages[0], self.season_filename)





if __name__ == "__main__":
    lebron = Player(78049)
