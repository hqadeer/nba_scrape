from nba_scrape import NBA
import unittest

class TestEntities(unittest.TestCase):

    def test_get_stat(self):

        '''Test the get_stat method of entities.py
        '''

        league = NBA()
        magic = league.get_player('magic johnson')
        self.assertEqual(magic.get_stat('asT', '1988-89'), 12.8)
        self.assertEqual(magic.get_stat('tOv', '1984-85'), 4.0)
        self.assertEqual(magic.get_stat('OREB', '1990-91', playoffs=True), 1.2)
        self.assertEqual(magic.get_stat('GS', 'career', playoffs=True), 186)
        self.assertEqual(magic.get_stat('team', '1985-86'), "LAL")
        self.assertEqual(magic.get_stat('pts', '2005-06'), None)
        #self.assertRaises(magic.get_stat('unicorn', '1999-00'), )


    def get_stats_test():
        return True

if __name__ == "__main__":

    temp = TestEntities()
    temp.test_get_stat()
