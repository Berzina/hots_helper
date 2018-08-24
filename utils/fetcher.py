import os
import requests
import time
from collections import namedtuple
from functools import partial
from threading import Thread, Event
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


STATISTICS_URL = 'https://hots.dog/api'
API_URL = 'http://hotsapi.net/api/v1'
BLIZZHERO_URL = 'http://blizzardheroes.ru'

BlizzHero = namedtuple('BlizzHero', ('hero', 'role', 'stats',
                                     'builds'))


def basic_fetch(url, appendix='', params={}):
    try:
        r = requests.get(url + appendix, params=params)
        response = r.json()
    except Exception:
        print('{} is unresponsive'.format(url + appendix))
    else:
        return response


fetch_heroes = partial(basic_fetch, API_URL, "/heroes")
fetch_hotsdog = partial(basic_fetch, STATISTICS_URL)


def fetch_blizzhero_page(link=BLIZZHERO_URL + '/heroes'):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        if os.environ.get("CHROME_BIN"):
            options.binary_location = os.environ.get("CHROME_BIN")

        browser = webdriver.Chrome(options=options,
                                   executable_path=os.environ.get(
                                    "CHROME_DRIVER_BIN"))

        browser.get(link)

        WebDriverWait(browser, timeout=10).until(
            lambda x: x.find_elements_by_xpath(
                '/html/body/div/div[2]/div/div[2]/div[1]/div[2]'))
        # ... other actions
        page = browser.page_source

        browser.close()

    except Exception as e:
        print(e)
    else:
        return page
