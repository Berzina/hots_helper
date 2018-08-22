import os
import requests
import time
from collections import namedtuple
from functools import singledispatch
from threading import Thread, Event
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# from utils.parser import BlizzParser

HAPPY_URL = 'http://happyzerg.ru/guides/builds'
STATISTICS_URL = 'https://hots.dog/'
API_URL = 'http://hotsapi.net/api/v1'

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


def fetch_blizzhero_page(link):
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
            lambda x: x.find_elements_by_xpath('/html/body/div/div[2]/div/div[2]/div[1]/div[2]'))
        # ... other actions
        page = browser.page_source

        browser.close()

    except Exception as e:
        print(e)
    else:
        return page


def fetch_blizzheroes_page(link='http://blizzardheroes.ru/heroes/'):
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
            lambda x: x.find_elements_by_xpath('/html/body/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[2]'))
        # ... other actions
        page = browser.page_source

        browser.close()

    except Exception as e:
        print(e)
    else:
        return page


def fetch_blizz_hero(hero):
    builds = []
    role = None
    stats = None
    page = None

    for ref in hero.build_refs:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')

            if os.environ.get("CHROME_BIN"):
                options.binary_location = os.environ.get("CHROME_BIN")

            browser = webdriver.Chrome(options=options,
                                       executable_path=os.environ.get(
                                        "CHROME_DRIVER_BIN"))

            browser.get(ref.link)

            WebDriverWait(browser, timeout=10).until(
                lambda x: x.find_element_by_id('talentid1'))
            # ... other actions
            page = browser.page_source

        except Exception as e:
            print(e)
            continue

        finally:
            bp = BlizzParser(ref.name, page)
            builds.append(bp.build)

            if not role and bp.parsed:
                role = bp.role
            elif role and not bp.parsed:
                role = role
            else:
                role = bp.role

            if not stats and bp.parsed:
                stats = bp.stats
            elif stats and not bp.parsed:
                stats = stats
            else:
                stats = bp.stats

            browser.close()

    print(BlizzHero(hero, role, stats, builds))

    return BlizzHero(hero, role, stats, builds)


def fetch_blizz(happy_heroes):

    blizz_heroes = []

    for hero in happy_heroes:
        blizz_heroes.append(fetch_blizz_hero(hero))

    return blizz_heroes


def fetch_data(url=HAPPY_URL):
    try:
        r = requests.get(url)
        page = r.text
    except Exception:
        print('{} is unresponsive'.format(url))
    else:
        return page


# class FetchingThread(Thread):
#     def __init__(self, event):
#         Thread.__init__(self)
#         self.stopped = event
#         self.daemon = True

#     def run(self):

#         while not self.stopped.wait(60*60*12):
#             fetch_data()
