from selenium import webdriver
from bs4 import BeautifulSoup
import traceback

def get_page(link):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    try:
        driver.get(str(link))
    except Exception as exc:
        traceback.print_exc()
        print(str(link), "is likely an invalid link")
        raise
    soup = BeautifulSoup(driver.page_source, features='lxml')
    driver.close()
    return soup
