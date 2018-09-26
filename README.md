# nba_scrape

An easy-to-use Python utility to scrape professional basketball data off stats.nba.com using Selenium and BeautifulSoup.

### Installation:

`pip install nba_scrape`

## Usage:

`from nba_scrape import NBA`

#### Get an instance of the NBA class:

`league = NBA()`

#### Get a player:

`player = league.get_player(player_name)`

OR

`player = league.get_player_by_id(id_number)`

#### Get a single stat:

`player.get_stat(stat_name, season)`

#### Get multiple stats (formatted as a dict with tuples as items):

`player.get_stats([stat1, stat2, stat3], season_range, mode=mode)`

(Possible modes are 'season', 'playoffs', or 'both'; 'season' is the default.)

### Current functionality:

1) Compile a list of all NBA players and their IDs when initializing the NBA class.

2) Easily load all regular season and playoff stats off a player's career page to a SQLite database. Only the player's name is required as input.

3) Retrieve all traditional stats and select advanced ones (such as True Shooting Percentage) via database queries; only the requested stats and seasons are required as input.

4) Browser-agnostic; uses the best available browser or raises an error if no supported browser is available.

5) Test suite to ensure correct statistics are returned.
