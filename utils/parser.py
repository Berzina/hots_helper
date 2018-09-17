# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from collections import namedtuple

from utils.filters import get_cyrillic, get_cyrillic_str, take_talent_by_name

from utils.fetcher import fetch_blizzhero_page, check_image, HOTSDOG_URL

from data.structures import *


def parse_builds(hero_talents, alt_hero_talents, best_builds):

    builds = []

    for build_name, build_info in best_builds.items():
        talents = []

        if build_info:
            t_lvl = 1

            for name in build_info['Build']:
                raw_talent = take_talent_by_name(hero_talents, name)
                alt_raw_talent = alt_hero_talents[name]
                alt_img = f'{HOTSDOG_URL}/img/talent/{name}.png'

                if raw_talent:
                    img = list(raw_talent['icon_url']
                               .values())[0]
                    img = img if check_image(img) else alt_img

                    talent = Talent2(name=raw_talent['name'],
                                     title=raw_talent['title'],
                                     idx=raw_talent['sort'],
                                     level=raw_talent['level'],
                                     ability=raw_talent['ability'],
                                     descr=raw_talent['description'],
                                     img=img)

                elif name in alt_hero_talents:
                    raw_talent = alt_hero_talents[name]
                    talent = Talent2(name=name,
                                     title=alt_raw_talent['Name'],
                                     idx=0,
                                     level=t_lvl,
                                     ability=0,
                                     descr=alt_raw_talent['Text'],
                                     img=alt_img)
                else:
                    raise Exception(f"Cannot find talent {name}!")

                talents.append(talent)

                t_lvl += 3 if t_lvl != 16 else 4

            build = Build2(name=build_name.capitalize(),
                           talents=talents,
                           count=build_info['Total'],
                           winrate=round(100*build_info['Winrate'], 2))

            builds.append(build)

    return builds


class APIParser:

    def __init__(self, data=None):
        self.hero_list = []
        self.json = data

        if data:
            self.parse()

    def parse(self):
        for hero in self.json:
            ru_name = get_cyrillic(hero["translations"])

            name = f"{ru_name.capitalize()} ({hero['name']})" \
                   if ru_name\
                   else hero["name"]

            alt_img = f'{HOTSDOG_URL}/img/hero_full/{hero["name"].lower()}.png'
            img = list(hero["icon_url"].values())[0]
            img = img if check_image(img) else alt_img

            self.hero_list.append(
                ApiHero(name,
                        ru_name.capitalize(),
                        hero["name"],
                        img,
                        hero["role"],
                        hero["type"]))


class BlizzParser:
    BLIZZHERO_URL = 'http://blizzardheroes.ru'

    def __init__(self, hero_list=[], page=None):
        self.hero_list = []
        self.bhero_list = []
        self.heroes = hero_list
        self.page = page

        if hero_list and page:
            print("Parse main page...")
            self.parse_main()
            print("Main parsed...")

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

            hero_block = soup.find('a', {'data-name': search_name})

            if hero_block:

                universe = hero_block.get("data-universe", "")
                link = hero_block.get("href", "")

                self.hero_list.append(
                    Hero(**api_hero._asdict(),
                         universe=universe,
                         blizz_link=self.BLIZZHERO_URL + link,
                         stats=stats))

    def get_hero(self, name):
        for hero in self.hero_list:

            if hero.name == name \
              or hero.ru_name == name \
              or hero.en_name == name:

                return hero
        return None

    def parse_bhero_list(self):
        for hero in self.hero_list:
            self.bhero_list.append(self.parse_bhero(hero))

        return self.bhero_list

    def parse_bhero(self, hero):

        one_hero, its_builds = self.parse_hero_page(hero)
        blizz_hero = BlizzHero(one_hero, builds=[])

        for build in its_builds:
            talents = self.parse_talents_page(build.link)
            build = Build(**{**build._asdict(), **{'talents': talents}})

            blizz_hero.builds.append(build)

        return blizz_hero

    def parse_bhero_by_name(self, name):
        hero = self.get_hero(name)

        if hero:
            return self.parse_bhero(hero)
        else:
            print(f"Can't find hero for: '{name}'")

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

        if guide_block:

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
