# nba-stats

A work-in-progress Python utility to easily scrape professional basketball data off stats.nba.com using Selenium and BeautifulSoup.

### Current functionality:

1) Compile a list of all NBA players and their IDs when initializing the NBA class.

2) Easily scrape all traditional regular season and playoff stats off a player's career page to a SQLite database. Only the player's name is required.

3) Retrieve all traditional stats and select advanced ones (such as True Shooting Percentage) via database queries; the user need only enter the requested stat and year.

4) Browser-agnostic; uses the best available browser or raises an error if no supported browser is available.

### To Do:

1) Support for a larger selection of advanced stats.

2) Support for team stats.

3) Write tests to check timing and correctness of code.

4) Make utility installable via Pip.
