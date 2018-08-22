import os
import requests
import time
from collections import namedtuple
from functools import singledispatch
from threading import Thread, Event
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# from utils.parser import BlizzParser

STATISTICS_URL = 'https://hots.dog/'
API_URL = 'http://hotsapi.net/api/v1'
BLIZZHERO_URL = 'http://blizzardheroes.ru'

BlizzHero = namedtuple('BlizzHero', ('hero', 'role', 'stats',
                                     'builds'))


def fetch_heroes(url=API_URL + "/heroes"):
    try:
        r = requests.get(url)
        response = r.json()
    except Exception:
        print('{} is unresponsive'.format(url))
    else:
        return response


def fetch_statistics():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    if os.environ.get("CHROME_BIN"):
        options.binary_location = os.environ.get("CHROME_BIN")

    browser = webdriver.Chrome(options=options,
                               executable_path=os.environ.get(
                                "CHROME_DRIVER_BIN"))

    browser.get(STATISTICS_URL)

    WebDriverWait(browser, timeout=10).until(
        lambda x: x.find_elements_by_xpath('//*[@id="root"]/main/section'))

    page = browser.page_source

    return page


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
