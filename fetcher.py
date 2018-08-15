import requests
import asyncio
from threading import Thread, Event

from utils.parser import HappyParser

HAPPY_URL = 'http://happyzerg.ru/guides/builds'
HAPPY_PAGE = ''
HAPPY_HEROES = HappyParser()


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

    HAPPY_HEROES = HappyParser(HAPPY_PAGE)


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
