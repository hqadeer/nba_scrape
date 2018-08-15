from helpers import get_page
from player import Player

class NBA:


    def __init__(self):


        page = get_page('http://stats.nba.com/players/list/?Historic=Y')

        self.players = {}
        for player in page.find_all("li", class_="players-list__name"):
            id = int(str(player.a['href']).split('/')[2].split('/')[0])
            name_comps = player.a.string.split(', ')
            if len(name_comps) == 2:
                name = (' '.join([name_comps[1], name_comps[0]])).lower()
            else:
                name = name_comps[0].lower()
            self.players[name] = id

    #def load_to_database(self):

    #ef get_player(self, id=None, name=None):

if __name__ == "__main__":
    we = NBA()
    print (we.players['lebron james'])
