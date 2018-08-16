from bs4 import BeautifulSoup
from collections import namedtuple

Hero = namedtuple('Hero', ('name', 'ru_name', 'en_name', 'image',
                           'build_refs'))
BuildRef = namedtuple('BuildRef', ('name', 'link'))


Build = namedtuple('Build', ('name', 'talents'))
Talent = namedtuple('Talent', ('idx', 'level', 'name', 'descr', 'img'))

Stats = namedtuple('Stats', ('damage', 'utility', 'survivability',
                             'complexity'))


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

        if not name:
            name = ' '.join([name.find("b").text
                             for name in names
                             if name.find("b")])

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


class BlizzParser:

    def __init__(self, build_name, data=None):

        self.talent_list = []
        self.page = data
        self.build = Build(build_name, [])
        self.role = ''
        self.stats = Stats(0, 0, 0, 0)
        self.parsed = False

        if data:
            self.parse()
            self.parsed = True

    def parse(self):
        self.soup = BeautifulSoup(self.page, features="html.parser")
        self.soup.prettify()

        talents = self.soup.find_all('div', {'class': 'level-talents'})

        for talent in talents:
            _, level, *idx_n_is_active = talent['class']

            name = talent.find('div', {'class': 'talent-title'}).text
            desc = talent.find('div', {'class': 'talent-desc'}).text
            img = talent.find('img')['src']

            if len(idx_n_is_active) == 2:
                idx, is_active = idx_n_is_active
                self.build.talents.append(Talent(idx.replace('talentid', ''),
                                                 level.replace('level', ''),
                                                 name,
                                                 desc,
                                                 img))

        self.role = self.soup.find('div', {'class': 'hero-role'})["class"][1]\
                             .replace("hero-role-", "")

        stat_damage = self.soup.find('div', {'class': 'hero-stats-damage'})
        damage = self.count_stat(stat_damage)

        stat_utility = self.soup.find('div', {'class': 'hero-stats-utility'})
        utility = self.count_stat(stat_utility)

        stat_survivability = self.soup.find('div',
                                            {'class':
                                             'hero-stats-survivability'})

        survivability = self.count_stat(stat_survivability)

        stat_complexity = self.soup.find('div', {'class':
                                                 'hero-stats-complexity'})

        complexity = self.count_stat(stat_complexity)

        self.stats = Stats(damage, utility, survivability, complexity)

    def count_stat(self, bs_obj):
        stat_blocks = bs_obj.find_all('div',
                                      {'class':
                                       'hero-stats-bar active'})

        return len(stat_blocks)
