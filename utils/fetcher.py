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


def basic_fetch(url, appendix='', params={}):
    try:
        r = requests.get(url + appendix, params=params)
        response = r.json()
    except Exception:
        print(f'{url + appendix} is unresponsive')
    else:
        return response


fetch_heroes = partial(basic_fetch, API_URL, "/heroes")
fetch_hotsdog = partial(basic_fetch, STATISTICS_URL)


def fetch_hero(en_name):
    return basic_fetch(API_URL, f"/heroes/{en_name}")


def fetch_hero_talents(en_name):
    return fetch_hero(en_name)["talents"]


def fetch_blizzhero_page(link=BLIZZHERO_URL + '/heroes'):
    print("Starting fetch hero page...")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        if os.environ.get("CHROME_BIN"):
            options.binary_location = os.environ.get("CHROME_BIN")

        browser = webdriver.Chrome(options=options,
                                   executable_path=os.environ.get(
                                    "CHROME_DRIVER_BIN"))

        browser.get(link)

        print("Waiting hero page...")

        WebDriverWait(browser, timeout=10).until(
            lambda x: x.find_elements_by_xpath(
                '/html/body/div/div[2]/div/div[2]/div[1]/div[2]'))
        # ... other actions
        page = browser.page_source

        print("Ready!...")

        browser.close()

    except Exception as e:
        print(e)
    else:
        return page
