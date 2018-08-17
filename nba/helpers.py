from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import traceback

def get_players(link):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(str(link))
    soup = BeautifulSoup(driver.page_source, features='lxml')
    driver.close()
    driver.quit()
    return soup

def get_player(link):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("user-agent=NBA")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(str(link))
    html = driver.find_element_by_tag_name("table").get_attribute("innerHTML")
    soup = BeautifulSoup(html, features='lxml')
    driver.close()
    driver.quit()
    return soup

def scrape_active_player(page, file_name):
    with open(file_name, 'w', newline='') as f:
        player_writer = csv.writer(f)
        stats = []
        for statistic in page.find_all("th"):
            file_string = str(statistic).split('>')[1].split('<')[0]
            stats.append(file_string)
        player_writer.writerow(stats)
        values = []
        for statistic in page.find_all("td"):
            if "class" in statistic.attrs:
                if "first" in statistic["class"]:
                    if len(values) > 0:
                        player_writer.writerow(values)
                    values = []
                    values.append(str(statistic)
                        .split('>')[1].split(' <')[0])
                elif "text" in statistic["class"]:
                    if statistic.a == None:
                        values.append(str(statistic).
                            split('>')[1].split('<')[0])
                    else:
                        values.append(str(statistic.a).
                            split('>')[1].split('<')[0])
            else:
                values.append((str(statistic).
                    split('>')[1].split('<')[0]))

def scrape_retired_player(page, file_name):
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
        player_writer.writerow(values)
        values = []
        for total in page.tfoot.find_all("td"):
            #if "class" in total.attrs and "text" in total["class"]:
            values.append(str(total).split('>')[1].split('<')[0])
        player_writer.writerow(values)
