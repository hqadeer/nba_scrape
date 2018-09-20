from nba_scrape import NBA
from nba_scrape import nba_exceptions
import unittest

class TestEntities(unittest.TestCase):

    def test_get_stat(self):
        '''Test the get_stat method of entities.py

        Specifically tests multiple instances, case insensitivity, None returns
        for valid stats and invalid queries, and TS% queries, and
        InvalidStatError raises for invalid stat queries.

        Also tests players that were traded mid-season, players that have no
        playoffs stats, null players, and players that have null values for
        many stats because they played before those were recorded.
        '''

        league = NBA()
        magic = league.get_player('mAGIC johnson')

        # Standard stat tests for a retired player.
        self.assertEqual(magic.get_stat('asT', '1988-89'), 12.8)
        self.assertEqual(magic.get_stat('tOv', '1984-85'), 4.0)
        self.assertEqual(magic.get_stat('OREB', '1990-91', playoffs=True), 1.2)
        self.assertEqual(magic.get_stat('GS', 'career', playoffs=True), 186)
        self.assertEqual(magic.get_stat('team', '1985-86'), "LAL")
        self.assertEqual(magic.get_stat('pts', '2005-06'), None)
        with self.assertRaises(nba_exceptions.InvalidStatError):
            magic.get_stat('unicorn', '1999-00')

        mario = league.get_player('mario chALmers')

        # Standard stat tests for an active player.
        self.assertEqual(mario.get_stat('team', '2015-16'), 'TOT')
        self.assertEqual(mario.get_stat('FT%', 'career', playoffs=True), 74.2)
        self.assertEqual(mario.get_stat('GP', '2017-18'), 66)
        self.assertEqual(mario.get_stat('3p%', '2010-11', playoffs=True), 38.1)
        self.assertEqual(mario.get_stat('fG%', '2017-18', playoffs=True), None)
        self.assertEqual(mario.get_stat('ft%', '2015-16'), 83.2)

        boogie = league.get_player('Demarcus Cousins')

        # Checking playoff stats of a player who's never been to the playoffs.
        self.assertEqual(boogie.get_stat('pts', 'career', playoffs=True), None)
        self.assertEqual(boogie.get_stat('pf', '2016-17', playoffs=True), None)
        with self.assertRaises(nba_exceptions.InvalidStatError):
            boogie.get_stat('unicorn', '2017-18', playoffs=True)

        booker = league.get_player('deVIN booker')

        # Same as above
        self.assertEqual(booker.get_stat('Blk', '2017-18'), 0.3)
        self.assertEqual(booker.get_stat('ast', 'career', playoffs=True), None)
        self.assertEqual(booker.get_stat('dreb', '2002-2342'), None)
        with self.assertRaises(nba_exceptions.InvalidStatError):
            booker.get_stat('unicorn', '2018-19', playoffs=True)

        kaj = league.get_player_by_id(76003)

        # Checking untracked stats of a retired player.
        self.assertEqual(kaj.get_stat('aGe', '1987-88'), 41)
        self.assertEqual(kaj.get_stat('age', 'career'), None)
        self.assertEqual(kaj.get_stat('3PM', '1985-86'), 0)
        self.assertEqual(kaj.get_stat('3pm', '1975-76'), None)
        self.assertEqual(kaj.get_stat('blk', '1972-73'), None)
        self.assertEqual(kaj.get_stat('tov', '1976-77'), None)

        # Checking stats of a player with no stats.
        no_stats = league.get_player('jaylen adams')
        self.assertEqual(no_stats.get_stat('pts', '1985-86'), None)
        self.assertEqual(no_stats.get_stat('ast', '1999-00', playoffs=True),
            None)
        with self.assertRaises(nba_exceptions.InvalidStatError):
            no_stats.get_stat('blobby', '2005-06')

        # Checking TS% queries.
        lebron = league.get_player('lebron james')
        self.assertTrue(abs(lebron.get_stat('ts%', '2017-18') - .621) < .2)
        self.assertTrue(abs(lebron.get_stat('ts%', '2013-14') - .649) < .2)
        self.assertTrue(abs(lebron.get_stat('ts%', '2015-16', playoffs=True)
            - .585) < .2)

    def test_get_stats(self):
        '''Test the get_stats method of entities.py

        Same tests as above (except TS% queries), but all of a player's
        requested stats are obtained in one query. Also uses different players.
        '''

        league = NBA()

        butler = league.get_player('jimmy butler')
        stats = butler.get_stats(['AST', 'TOV', 'OREB'], '2012-16')
        print(stats)


if __name__ == "__main__":

    unittest.main()
