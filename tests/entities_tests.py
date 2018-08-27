from nba_scrape import NBA

def get_stat_test():

    '''Test the get_stat method of entities.py
    '''

    magic = NBA.get_player('MaGiC JOHNSON')
    assert magic.get_stat('asT', '1988-89') == 12.8
    assert magic.get_stat('tOv', '1984-85') == 4.0
    assert magic.get_stat('OREB', '1990-91', playoffs=True) == 1.2
    assert magic.get_stat('GS', 'career', playoffs=True) == 186

if __name__ == "__main__":

    get_stat_test()
