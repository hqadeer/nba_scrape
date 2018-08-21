# NBA Stats

A work-in-progress Python utility to scrape professional basketball data off stats.nba.com using Selenium and BeautifulSoup.

### Current functionality:

1) Obtain a player's numeric ID via the NBA class.

2) Scrape all traditional regular season and playoff stats off a player's career page to a SQLite database.

3) Compute TS% based on several traditional stats.

4) Retrieve specific stats or entire player profile with database queries.

5) Detect if user has a supported browser

### To Do:

1) Support for more advanced stats.

2) Support for team stats.

3) Wrapper support for more sophisticated database queries. I.e., pulling a player's stats for a specified range of seasons.

4) Write tests to check timing and correctness of code.

5) Make utility installable via Pip.
