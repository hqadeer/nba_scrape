import os
import errno
import helpers

class Player:


    def __init__(self, id):

        url = "".join(["http://stats.nba.com/player/", str(id), '/'])
        self.file_name = "".join(['nba/data/', str(id), '.csv'])
        if not os.path.isfile(self.file_name):
            if not os.path.isdir(os.path.dirname(self.file_name)):
                try:
                    os.makedirs(os.path.dirname(self.file_name))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            page = helpers.get_player(url)
            if page.tfoot is None:
                helpers.scrape_active_player(page, self.file_name)
            else:
                helpers.scrape_retired_player(page, self.file_name)


if __name__ == "__main__":
    lebron = Player(78049)
