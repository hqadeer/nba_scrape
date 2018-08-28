from nba_scrape import NBA
from nba_scrape import nba_exceptions
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
        with self.assertRaises(nba_exceptions.InvalidStatError):
            magic.get_stat('unicorn', '1999-00')

        mario = league.get_player('mario chalmers')
        self.assertEqual(mario.get_stat('team', '2015-16'), 'TOT')
        self.assertEqual(mario.get_stat('FT%', 'career', playoffs=True), 74.2)
        self.assertEqual(mario.get_stat('GP', '2017-18'), 66)
        self.assertEqual(mario.get_stat('3p%', '2010-11', playoffs=True), 38.1)
        self.assertEqual(mario.get_stat('fG%', '2017-18', playoffs=True), 5)
        self.assertEqual(mario.get_stat('ft%', '2015-16'), 83.2)



    def test_get_stats(self):
        self.assertEqual(2, 2)

if __name__ == "__main__":

    unittest.main()
