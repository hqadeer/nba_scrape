from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as selexc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import traceback
import sys

browser = "chrome"

def detect_browser():


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
        print("Using PhantomJS, which is an unsupported browser.",
            "Consider installing Chrome or Firefox.", file=sys.stderr)
        driver.quit()
        return

    try:
        driver = webdriver.Opera()
    except (selexc.WebDriverException, FileNotFoundError) as exc:
        pass
    else:
        browser = "opera"
        print("Using Opera. Opera does not support headless mode, so",
            "consider installing Chrome or Firefox.", file=sys.stderr)
        return

    try:
        driver = webdriver.Safari()
    except (selexc.WebDriverException, FileNotFoundError) as exc:
        pass
    except selexc.SessionNotCreatedException:
        print("To use Safari for scraping, enable 'Allow Remote",
            "Automation' option in Safari's Develop menu. Safari does not",
            "support headless mode, so consider installing Chrome or Firefox",
            file=sys.stderr)
    else:
        browser = "safari"
        print("Using Safari. Safari does not support headless mode, so",
            "consider installing Chrome or Firefox.", file=sys.stderr)
        return

    print("No supported browsers found. Install Chrome or Firefox for",
        "optimal usage.", file=sys.stderr)
    raise

def get_players(link):


    global browser

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('user-agent=Kobe')
        driver = webdriver.Chrome(chrome_options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument('headless')
        options.add_argument('user-agent=Kobe')
        driver = webdriver.Firefox(firefox_options=options)
    elif browser == "PhantomJS":
        driver = webdriver.PhantomJS()
    elif browser == "opera":
        driver = webdriver.Opera()
    elif browser == "safari":
        driver = webdriver.Safari()
    else:
        print("No browser found.", file=sys.stderr)
        raise
    driver.get(str(link))
    soup = BeautifulSoup(driver.page_source, features='lxml')
    driver.quit()
    return soup

def get_player(link, mode="both"):


    global browser

    print(browser)
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('user-agent=Kobe')
        driver = webdriver.Chrome(chrome_options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument('headless')
        options.add_argument('user-agent=Kobe')
        driver = webdriver.Firefox(firefox_options=options)
    elif browser == "PhantomJS":
        driver = webdriver.PhantomJS()
    elif browser == "opera":
        driver = webdriver.Opera()
    elif browser == "safari":
        driver = webdriver.Safari()
    else:
        print("No browser found.", file=sys.stderr)
        raise

    driver.get(str(link))
    if mode == "season":
        try:
            html = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            return [BeautifulSoup(html.get_attribute('innerHTML'),
                features='lxml')]
        finally:
            driver.quit()
    try:
        htmls = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
        )
        soup = BeautifulSoup(htmls[0].get_attribute('innerHTML'),
            features='lxml')
        psoup = soup
        psoup = BeautifulSoup(htmls[2].get_attribute('innerHTML'),
                features='lxml')
        if mode == "playoffs":
            return [psoup]
        elif mode == "both":
            return [soup, psoup]
    finally:
        driver.quit()

def scrape_player(page, file_name):


    with open(file_name, 'w', newline='') as f:
        player_writer = csv.writer(f)
        stats = []
        for statistic in page.find_all("th"):
            if "class" in statistic.attrs and "text" in statistic["class"]:
                tag = statistic.span
            else:
                tag = statistic
            file_string = str(tag).split('>')[1].split('<')[0]
            stats.append(file_string)
        player_writer.writerow(stats)
        values = []
        for statistic in page.tbody.find_all("td"):
            if "class" in statistic.attrs:
                if "player" in statistic["class"]:
                    if len(values) > 0:
                        player_writer.writerow(values)
                    values = []
                    values.append(str(statistic.a['href']).split('=')[1].
                        split('&')[0])
                elif "text" in statistic["class"]:
                    values.append(str(statistic.span).split('>')[1].
                        split('<')[0])
            else:
                values.append((str(statistic).
                    split('>')[1].split('<')[0]))
        if len(values) > 0:
            player_writer.writerow(values)
        values = []
        for total in page.tfoot.find_all("td"):
            values.append(str(total).split('>')[1].split('<')[0])
        player_writer.writerow(values)
