from selenium import webdriver
from bs4 import BeautifulSoup

import traceback

def get_players(link):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(str(link))
    soup = BeautifulSoup(driver.page_source, features='lxml')
    driver.close()
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
    return soup
