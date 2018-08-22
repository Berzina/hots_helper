# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from collections import namedtuple

from utils.filters import get_cyrillic, get_cyrillic_str

from utils.fetcher import fetch_blizzhero_page

from data.storage import set_blizz, get_blizz

ApiHero = namedtuple('ApiHero', ('name', 'ru_name', 'en_name', 'image',
                                 'role', 'type'))

Hero = namedtuple('Hero', ('name', 'ru_name', 'en_name', 'image',
                           'role', 'type', 'universe', 'blizz_link',
                           'stats'))

Stats = namedtuple('Stats', ('damage', 'utility', 'survivability',
                             'complexity'))

Build = namedtuple('Build', ('name', 'talents', 'link'))
Talent = namedtuple('Talent', ('idx', 'level', 'name', 'descr', 'img'))

BlizzHero = namedtuple('BlizzHero', ('hero', 'builds'))


class APIParser:

    def __init__(self, data=None):
        self.hero_list = []
        self.json = data

        if data:
            self.parse()

    def parse(self):
        for hero in self.json:
            ru_name = get_cyrillic(hero["translations"])

            self.hero_list.append(
                ApiHero("{ru_name} ({en_name})"
                        .format(ru_name=ru_name.capitalize(),
                                en_name=hero["name"]),

                        ru_name.capitalize(),
                        hero["name"],
                        list(hero["icon_url"].values())[0],
                        hero["role"],
                        hero["type"]))


class BlizzParser:
    BLIZZHERO_URL = 'http://blizzardheroes.ru'

    def __init__(self, hero_list=[], page=None, update_on_loading=False):
        self.hero_list = []
        self.bhero_list = []
        self.heroes = hero_list
        self.page = page
        self.update_on_loading = update_on_loading

        if hero_list and page:
            self.parse()

    def parse(self):
        self.parse_main()

        for hero in self.hero_list:

            one_hero, its_builds = self.parse_hero_page(hero)
            blizz_hero = BlizzHero(one_hero, builds=[])

            for build in its_builds:
                talents = self.parse_talents_page(build.link)
                build = Build(**{**build._asdict(), **{'talents': talents}})

                blizz_hero.builds.append(build)

                if self.update_on_loading:
                    set_blizz([blizz_hero], replace=False)
                    print("Saved to bin: {}".format(blizz_hero.hero.name))
                    print("in bin now: {}"
                          .format(" ".join([bhero.hero.name
                                            for bhero in get_blizz()])))

            self.bhero_list.append(blizz_hero)

            print("Loaded: {}".format(blizz_hero.hero.name))

        return self.bhero_list

    def parse_main(self):
        stats = Stats(0, 0, 0, 0)

        soup = BeautifulSoup(self.page, features="html.parser")
        soup.prettify()

        for api_hero in self.heroes:
            ru_name = api_hero.ru_name.lower()

            ru_name = ru_name.split()[1] \
                      if len(ru_name.split()) == 2 and ru_name != 'ли ли'\
                      else ru_name

            if api_hero.en_name == 'E.T.C.':
                search_name = 'е.т.с.'
            elif api_hero.en_name == 'D.Va':
                search_name = 'd.va'
            else:
                search_name = ru_name

            hero_block = soup.find('a', {'data-name': ru_name})

            if hero_block:

                universe = hero_block.get("data-universe", "")
                link = hero_block.get("href", "")

                self.hero_list.append(
                    Hero(**api_hero._asdict(),
                         universe=universe,
                         blizz_link=self.BLIZZHERO_URL + link,
                         stats=stats))

    def parse_hero_page(self, hero):
        page = fetch_blizzhero_page(hero.blizz_link)

        if page:
            soup = BeautifulSoup(page, features="html.parser")
            soup.prettify()

            stats = self.get_stats(soup)
            builds = self.get_builds(soup)

            return Hero(**{**hero._asdict(), **{'stats': stats}}), builds
        else:
            return hero, []

    def get_stats(self, bs_obj):
        stat_damage = bs_obj.find('div', {'class': 'hero-stats-damage'})
        damage = self.count_stat(stat_damage)

        stat_utility = bs_obj.find('div', {'class': 'hero-stats-utility'})
        utility = self.count_stat(stat_utility)

        stat_survivability = bs_obj.find('div',
                                         {'class':
                                          'hero-stats-survivability'})

        survivability = self.count_stat(stat_survivability)

        stat_complexity = bs_obj.find('div', {'class':
                                              'hero-stats-complexity'})

        complexity = self.count_stat(stat_complexity)

        stats = Stats(damage, utility, survivability, complexity)

        return stats

    def get_builds(self, bs_obj):
        talents = []
        builds = []

        guide_block = bs_obj.find('div', {'class': 'guides-list'})

        guide_blocks = guide_block.find_all('a')

        guide_blocks = guide_blocks if len(guide_blocks) <= 2 \
                                    else guide_blocks[:2]

        for block in guide_blocks:
            name = block.find('div', {'class': 'title'}).text
            link = self.BLIZZHERO_URL + block.get('href', "")

            builds.append(Build(name, [], link))

        return builds

    def parse_talents_page(self, link):
        talents = []
        idx = 0

        page = fetch_blizzhero_page(link)

        if page:
            soup = BeautifulSoup(page, features="html.parser")
            soup.prettify()

            talent_row = soup.find('div', {'class': 'single-build'})

            for talent in talent_row.find_all('div', {'class': 'single'}):
                level = talent.find('div', {'class': 'single-level'}).text

                talent_info = talent.find('div', {'class': 'single-talent'})

                img = self.BLIZZHERO_URL + talent_info.find('img')['src']

                name = talent_info.find('div',
                                        {'class':
                                         'tooltipe-talent-title'}).text

                name = get_cyrillic_str(name)

                descr = talent_info.find('div',
                                         {'class':
                                          'tooltipe-talent-text'}).text

                talents.append(Talent(idx, level, name, descr, img))

        return talents

    def count_stat(self, bs_obj):
        stat_blocks = bs_obj.find_all('div',
                                      {'class':
                                       'hero-stats-bar active'})

        return len(stat_blocks)
