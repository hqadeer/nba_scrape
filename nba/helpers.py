from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import traceback
import time

#def setup():




def get_players(link):


    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(str(link))
    soup = BeautifulSoup(driver.page_source, features='lxml')
    driver.quit()
    return soup

def get_player(link, mode="both"):


    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("user-agent=NBA")
    driver = webdriver.Chrome(chrome_options=options)
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
