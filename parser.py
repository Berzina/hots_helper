import requests
from bs4 import BeautifulSoup
from collections import namedtuple

HAPPY_URL = 'http://happyzerg.ru/guides/builds'

Hero = namedtuple('Hero', ('name', 'image', 'builds'))
Build = namedtuple('Build', ('name', 'link'))


class HappyParser:

    def __init__(self, url=HAPPY_URL):

        r = requests.get(url)

        self.page = r.text
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
