import os
import requests
import asyncio
from collections import namedtuple
from threading import Thread, Event
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from utils.parser import HappyParser, BlizzParser
from utils.views import open_build

HAPPY_URL = 'http://happyzerg.ru/guides/builds'
HAPPY_PAGE = ''
HAPPY_HEROES = HappyParser()

PREFETCHED = {}

BlizzHero = namedtuple('BlizzHero', ('hero', 'role', 'character',
                                     'builds'))


def get_hero_view_by_name(name):
    some_heroes = HAPPY_HEROES.take_by_name(name)

    if not some_heroes:
        return 'Found no heroes for you :( Is {} hero name correct?'\
               .format(name)
    elif len(some_heroes) == 1:
        bh = collect_hero(some_heroes[0])
        return open_build(bh)
    else:
        return HAPPY_HEROES.prepare_build_response(name)


def collect_hero(hero):

    bh = BlizzHero(hero, 'role', 'character', [])

    for ref in hero.build_refs:
        page = PREFETCHED[ref.link] if ref.link in PREFETCHED \
                                    else fetch_blizz(ref.link)
        bp = BlizzParser(ref.name, page)
        bh.builds.append(bp.build)

    return bh


def fetch_blizz(url):

    global PREFETCHED

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    if os.environ.get("CHROME_BIN"):
        options.binary_location = os.environ.get("CHROME_BIN")

    browser = webdriver.Chrome(options=options,
                               executable_path=os.environ.get(
                                "CHROME_DRIVER_BIN"))

    browser.get(url)

    WebDriverWait(browser, timeout=10).until(
        lambda x: x.find_element_by_id('talentid1'))
    # ... other actions
    generated_html = browser.page_source
    browser.quit()

    PREFETCHED[url] = generated_html

    return generated_html


def fetch_data(url=HAPPY_URL):
    try:
        r = requests.get(url)
        page = r.text
    except Exception:
        print('{} is unresponsive'.format(url))
    else:
        global HAPPY_PAGE

        HAPPY_PAGE = page


def update_heroes():
    global HAPPY_HEROES
    global PREFETCHED

    HAPPY_HEROES = HappyParser(HAPPY_PAGE)

    PREFETCHED = {}

    for hero in HAPPY_HEROES.hero_list:
        for ref in hero.build_refs:
            PREFETCHED[ref.link] = fetch_blizz(ref.link)


fetch_data()
update_heroes()


class FetchingThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
        self.daemon = True

    def run(self):
        while not self.stopped.wait(60*60*12):
            fetch_data()
            update_heroes()


def fetch_data_hourly():
    stopFlag = Event()
    thread = FetchingThread(stopFlag)
    thread.start()
    # this will stop the timer
    #stopFlag.set()


fetch_data_hourly()
