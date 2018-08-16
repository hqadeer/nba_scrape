import os
import errno
from helpers import get_player

class Player:


    def __init__(self, id):
        url = "".join(["http://stats.nba.com/player/", str(id), '/'])
        page = get_player(url)
        file_name = "".join(['nba/data/', str(id), '.txt'])
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        with open(file_name, 'w') as f:
            for statistic in page.find_all("th"):
                file_string = str(statistic).split('>')[1].split('<')[0] + ','
                f.write(file_string)
            for statistic in page.find_all("td"):
                if "class" in statistic.attrs:
                    if "first" in statistic["class"]:
                        file_string = "".join(['\n',
                            str(statistic).split('>')[1].split(' <')[0], ','])
                        f.write(file_string)
                    elif "text" in statistic["class"]:
                        file_string = (str(statistic.a).split('>')[1].split('<')[0]
                            + ',')
                        f.write(file_string)
                else:
                    file_string = (str(statistic).split('>')[1].split('<')[0] +
                        ',')
                    f.write(file_string)



if __name__ == "__main__":
    lebron = Player(2544)
