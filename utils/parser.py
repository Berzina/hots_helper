from bs4 import BeautifulSoup
from collections import namedtuple

Hero = namedtuple('Hero', ('name', 'ru_name', 'en_name', 'image',
                           'build_refs'))
BuildRef = namedtuple('BuildRef', ('name', 'link'))


Build = namedtuple('Build', ('name', 'talents'))
Talent = namedtuple('Talent', ('idx', 'name', 'descr'))


BlizzHero = namedtuple('BlizzHero', ('hero', 'role', 'character',
                                     'builds'))


class HappyParser:

    def __init__(self, data=None):

        self.hero_list = []
        self.page = data

        if data:
            self.parse()

    def parse(self):
        self.soup = BeautifulSoup(self.page, features="html.parser")
        self.soup.prettify()

        with_headers = self.soup.find_all('tr')

        for row in with_headers[1:]:
            img_and_name, s, t = row.find_all('td')

            image, name, ru_name, en_name = self.get_img_n_name(img_and_name)
            builds = self.get_builds(s)

            self.hero_list.append(Hero(name, ru_name, en_name, image, builds))

    def get_img_n_name(self, img_n_name: str):

        ru_name = None
        en_name = None

        img, *names = img_n_name.find_all('span')

        if img.find("img"):
            image = img.find("img")['src']
        else:
            image = None

        name = ' '.join([name.find("strong").text
                         for name in names
                         if name.find("strong")])

        if name:
            ru_name, *en_name = name.split()
            en_name = en_name[0][1:-1] if en_name else None

        return image, name, ru_name, en_name

    def get_builds(self, s):
        builds = []

        for build in s.find_all("li"):
            name = build.find("a").text
            link = build.find("a")["href"]

            builds.append(BuildRef(name, link))

        return builds

    def take_by_name(self, name):
        matching = [hero for hero in self.hero_list
                    if name.lower() in hero.name.lower()]

        def match_score(hero):
            ru_pos = hero.ru_name.lower().find(name.lower())
            en_pos = hero.en_name.lower().find(name.lower())

            return ru_pos if ru_pos > en_pos else en_pos

        matching.sort(key=lambda x: match_score(x))

        return matching

    def prepare_build_response(self, name=None):

        response = ''

        if name is None:
            matching = self.hero_list
        else:
            matching = self.take_by_name(name)

        for hero in matching:
            response += '''
**{name}**


__Builds:__

{blist}


'''\
.format(name=hero.name,
        blist='\n'.join(['* {bname}: {blink}'
                         .format(bname=build.name,
                                 blink=build.link)
                         for build in hero.build_refs]))

        return response if response else "Can't find your hero, dude :("


class BlizzParser:

    def __init__(self, data=None):

        self.hero_list = []
        self.page = data

        if data:
            self.parse()

    def parse(self):
        self.soup = BeautifulSoup(self.page, features="html.parser")
        self.soup.prettify()

        print(self.soup)
