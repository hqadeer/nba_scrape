import os
import errno
import helpers

class Player:


    def __init__(self, id):

        season_url = "".join(["http://stats.nba.com/player/", str(id),
            '/'])
        self.season_filename = "".join(['nba/data/players/season/',
            str(id), '.csv'])
        playoffs_url = season_url + "?Season=2017-18&SeasonType=Playoffs"
        self.playoffs_filename = "".join(['nba/data/players/playoffs/',
            str(id), '.csv'])
        pair = [(season_url, self.season_filename),
            (playoffs_url, self.playoffs_filename)]
        for filetype in pair:
            if not os.path.isfile(filetype[1]):
                if not os.path.isdir(os.path.dirname(filetype[1])):
                    try:
                        os.makedirs(os.path.dirname(filetype[1]))
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise
                page = helpers.get_player(filetype[0])
                if page.tfoot is None:
                    helpers.scrape_active_player(page, filetype[1])
                else:
                    helpers.scrape_retired_player(page, filetype[1])



if __name__ == "__main__":
    lebron = Player(78049)
