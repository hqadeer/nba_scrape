# nba-stats

A work-in-progress Python utility to easily scrape professional basketball data off stats.nba.com using Selenium and BeautifulSoup.

### Current functionality:

1) Compile a list of all NBA players and their IDs when initializing the NBA class.

2) Easily load all regular season and playoff stats off a player's career page to a SQLite database. Only the player's name is required as input.

3) Retrieve all traditional stats and select advanced ones (such as True Shooting Percentage) via database queries; only the requested stats and seasons are required as input.

4) Browser-agnostic; uses the best available browser or raises an error if no supported browser is available.

### To Do:

Write tests to check timing and correctness of code.
