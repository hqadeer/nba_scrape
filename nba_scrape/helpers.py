from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as selexc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from nba_scrape.nba_exceptions import InvalidBrowserError
from bs4 import BeautifulSoup
import sqlite3
import traceback
import sys

browser = "chrome"

def detect_browser():
    '''Detect user's browser and set browser to be the best available one.

    Raise InvalidBrowserError if no supported browser is found.
    '''

    global browser

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome()
    except (selexc.WebDriverException, FileNotFoundError) as exc:
        pass
    else:
        driver.quit()
        return

    try:
        options = webdriver.FirefoxOptions()
        options.add_argument('headless')
        driver = webdriver.Firefox()
    except (selexc.WebDriverException, FileNotFoundError) as exc:
        pass
    else:
        browser = "firefox"
        driver.quit()
        return

    try:
        driver = webdriver.PhantomJS()
    except (selexc.WebDriverException, FileNotFoundError) as exc:
        pass
    else:
        browser = "PhantomJS"
        print('''Using PhantomJS, which is an unsupported browser.
            Consider installing Chrome or Firefox.''', file=sys.stderr)
        driver.quit()
        return

    try:
        driver = webdriver.Opera()
    except (selexc.WebDriverException, FileNotFoundError) as exc:
        pass
    else:
        browser = "opera"
        driver.quit()
        print('''Using Opera. Opera does not support headless mode, so
            consider installing Chrome or Firefox.''', file=sys.stderr)
        return

    try:
        driver = webdriver.Safari()
    except (selexc.WebDriverException, FileNotFoundError) as exc:
        pass
    except selexc.SessionNotCreatedException:
        driver.quit()
        print("To use Safari for scraping, enable 'Allow Remote",
              "Automation' option in Safari's Develop menu. Safari does not",
              "support headless mode, so consider installing Chrome or Firefox",
              file=sys.stderr)
    else:
        driver.quit()
        browser = "safari"
        print("Using Safari. Safari does not support headless mode, so",
              "consider installing Chrome or Firefox.", file=sys.stderr)
        return

    raise InvalidBrowserError('''No supported browsers found. Install Chrome or
        Firefox for optimal usage.''')

def get_players(link):
    ''' Return BeautifulSoup page of stats.nba.com's list of players.

    link -- URL to NBA's list of all players.
    '''

    global browser

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('user-agent=Kobe')
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument('headless')
        options.add_argument('user-agent=Kobe')
        driver = webdriver.Firefox(options=options)
    elif browser == "PhantomJS":
        driver = webdriver.PhantomJS()
    elif browser == "opera":
        driver = webdriver.Opera()
    elif browser == "safari":
        driver = webdriver.Safari()
    else:
        raise InvalidBrowserError("No valid browser found.")

    driver.get(str(link))
    soup = BeautifulSoup(driver.page_source, features='lxml')
    driver.quit()
    return soup

def get_player_trad(link, mode="both"):
    '''Return a list of html tables off an NBA player's stats page.

    link (str) -- URL to the player's career page
    mode (str) -- 'season', 'playoffs', or 'both'. Determines what tables
                  are returned.
    '''

    if mode not in ["both", "season", "playoffs"]:
        raise ValueError("Invalid value for mode.")

    global browser

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('user-agent=Kobe')
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument('headless')
        options.add_argument('user-agent=Kobe')
        driver = webdriver.Firefox(options=options)
    elif browser == "PhantomJS":
        driver = webdriver.PhantomJS()
    elif browser == "opera":
        driver = webdriver.Opera()
    elif browser == "safari":
        driver = webdriver.Safari()
    else:
        raise InvalidBrowserError("No valid browser found.")

    driver.get(str(link))
    if mode.lower() == "season":
        try:
            html = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "nba-stat-table"))
            )
            soup = BeautifulSoup(html.get_attribute('innerHTML'),
                                 features='lxml')
            if (soup.find_all("div", class_="nba-stat-table__caption")[0]
                    .span.string) == "Career Regular Season Stats":
                return soup.table
            else:
                return
        finally:
            driver.quit()
    else:
        try:
            returns = [None, None]
            try:
                htmls = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located(
                            (By.TAG_NAME, "nba-stat-table"))
                )
            except TimeoutException:
                return returns
            soup = BeautifulSoup(htmls[1].get_attribute('innerHTML'),
                                 features='lxml')
            if (soup.find_all("div", class_="nba-stat-table__caption")[0]
                    .span.string) == "Career Playoffs Stats":
                if mode.lower() == "playoffs":
                    return soup.table
                else:
                    returns[1] = soup.table

            if mode.lower() == "both":
                soup = BeautifulSoup(htmls[0].get_attribute('innerHTML'),
                                     features='lxml')
                if (soup.find_all("div", class_="nba-stat-table__caption")[0]
                        .span.string) == "Career Regular Season Stats":
                    returns[0] = soup.table

                return returns

        finally:
            driver.quit()

def create_empty_row(id):
    '''Creates empty row in tradstats table.

    Used as a placeholder for listed players with no stats. This way, calls to
    these players do not incur Selenium bottlenecks.
    '''

    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute('''INSERT INTO tradstats(ID) VALUES(?)''', (id,))
    db.commit()
    db.close()

def scrape_player_trad(page, id, playoffs=False):
    '''Reads player data off an html page and add it to a database table.

    Creates database table for a player with appropriate headers if it doesn't
    already exist.

    page (BeautifulSoup) -- html page to be read by the method.
    id (int) -- id of the player being read
    playoffs (bool) -- specifies whether playoff or regular season stats will
    be added to the database.
    '''

    if not playoffs:
        pcheck = 0
    else:
        pcheck = 1

    db = sqlite3.connect('data.db')
    player_writer = db.cursor()

    try:
        player_writer.execute('''CREATE TABLE tradstats(ID INTEGER, PLAYOFFS
            INTEGER)''')
    except sqlite3.OperationalError:
        pass
    else:
        player_writer.execute('''CREATE INDEX id_index on tradstats (ID)''')
        for statistic in page.find_all("th"):
            if "class" in statistic.attrs and "text" in statistic["class"]:
                tag = statistic.span
            else:
                tag = statistic
            file_string = str(tag).split('>')[1].split('<')[0]
            if file_string in ["Season", "TEAM"]:
                player_writer.execute('''ALTER TABLE tradstats ADD %s
                    TEXT''' % file_string)
            else:
                if '%' in file_string:
                    file_string = file_string.replace("%", "percent")
                if '3' in file_string:
                    file_string = file_string.replace("3", "three")
                player_writer.execute('''ALTER TABLE tradstats ADD %s
                    NUMERIC''' % file_string)
        db.commit()

    # Update table even if it already exists:

    values = []
    entries = []
    for statistic in page.tbody.find_all("td"):
        if "class" in statistic.attrs:
            if "player" in statistic["class"]:
                if len(values) > 0:
                    entries.append(tuple(values))
                values = [id, pcheck]
                values.append(statistic.a.string)
            elif "text" in statistic["class"]:
                values.append(statistic.span.string)
        else:
            temp = statistic.string
            if temp in ['', '-', None]:
                values.append(None)
            else:
                values.append(float(statistic.string))
    if len(values) > 0:
        entries.append(tuple(values))
    values = [id, pcheck]
    for total in page.tfoot.find_all("td"):
        value = total.string
        if value in ["", "-"]:
            value = None
        if value == "Overall: ":
            value = "CAREER"
        values.append(value)

    entries.append(tuple(values))
    place = ', '.join('?' * len(values))
    player_writer.executemany('''INSERT INTO tradstats values (%s)''' %
                              place, entries)
    db.commit()
    db.close()

def scrub(text):
    '''Ensures against SQL injections for user-provided database queries.

    Checks against a list of malicious characters (given by bad_chars).

    text (str) -- String being tested; this is usually user input for a
    database query.
    '''

    if not isinstance(text, str):
        raise ValueError("Invalid input passed to scrub; expected str.")
    bad_chars = [';', 'OR ', ' ']
    if any(i in text for i in bad_chars):
        raise ValueError('''Invalid input passed for database query. Please
            don't hack me.''')
