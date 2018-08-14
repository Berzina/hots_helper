import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import threading

HAPPY_URL = 'http://happyzerg.ru/guides/builds'
HAPPY_PAGE = ''

Hero = namedtuple('Hero', ('name', 'image', 'builds'))
Build = namedtuple('Build', ('name', 'link'))


class HappyParser:

    def __init__(self, data=HAPPY_PAGE):

        if not data:
            fetch_data()

        self.page = HAPPY_PAGE
        self.hero_list = []

    def parse(self):
        self.soup = BeautifulSoup(self.page)
        self.soup.prettify()

        with_headers = self.soup.find_all('tr')

        for row in with_headers[1:]:
            img_and_name, s, t = row.find_all('td')

            image, name = self.get_img_n_name(img_and_name)
            builds = self.get_builds(s)

            self.hero_list.append(Hero(name, image, builds))

    def get_img_n_name(self, img_n_name: str):

        img, *names = img_n_name.find_all('span')

        if img.find("img"):
            image = img.find("img")['src']
        else:
            image = None

        name = ' '.join([name.find("strong").text
                         for name in names
                         if name.find("strong")])

        return image, name

    def get_builds(self, s):
        builds = []

        for build in s.find_all("li"):
            name = build.find("a").text
            link = build.find("a")["href"]

            builds.append(Build(name, link))

        return builds

    def take_by_name(self, name):
        return [hero for hero in self.hero_list
                if name.lower() in hero.name.lower()]

    def prepare_build_response(self, name=None):

        response = ''

        if name is None:
            matching = self.hero_list
        else:
            matching = self.take_by_name(name)

        for hero in matching:
            response += '''
*{name}*

_Builds:_
{blist}


'''\
.format(name=hero.name,
        blist='\n'.join(['- {bname}: {blink}'
                         .format(bname=build.name,
                                 blink=build.link)
                         for build in hero.builds]))

        return response if response else "Can't find your hero, dude :("


def fetch_data(url=HAPPY_URL):
    try:
        r = requests.get(url)
        page = r.text
    except Exception:
        print('{} is unresponsive'.format(url))
    else:
        global HAPPY_PAGE
        HAPPY_PAGE = page


def fetch_data_hourly():
    threading.Timer(3600.0, fetch_data).start()
