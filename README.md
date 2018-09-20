# nba_scrape

An easy-to-use Python utility to scrape professional basketball data off stats.nba.com using Selenium and BeautifulSoup.

### Installation:

`pip install nba_scrape`

### Current functionality:

1) Compile a list of all NBA players and their IDs when initializing the NBA class.

2) Easily load all regular season and playoff stats off a player's career page to a SQLite database. Only the player's name is required as input.

3) Retrieve all traditional stats and select advanced ones (such as True Shooting Percentage) via database queries; only the requested stats and seasons are required as input.

4) Browser-agnostic; uses the best available browser or raises an error if no supported browser is available.

5) Test suite to ensure correct statistics are returned.
