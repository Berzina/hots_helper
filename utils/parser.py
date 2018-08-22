from bs4 import BeautifulSoup
from collections import namedtuple
from itertools import dropwhile

from utils.filters import is_cyrillic

from utils.fetcher import fetch_blizzhero_page

Hero = namedtuple('Hero', ('name', 'ru_name', 'en_name', 'image',
                           'build_refs'))

ApiHero = namedtuple('ApiHero', ('name', 'ru_name', 'en_name', 'image',
                                 'role', 'type'))

BuildRef = namedtuple('BuildRef', ('name', 'link'))


Build = namedtuple('Build', ('name', 'talents'))
Talent = namedtuple('Talent', ('idx', 'level', 'name', 'descr', 'img'))

Stats = namedtuple('Stats', ('damage', 'utility', 'survivability',
                             'complexity'))

Build2 = namedtuple('Build2', ('name', 'talents', 'link'))
Talent2 = namedtuple('Talent2', ('level', 'name', 'descr', 'img'))
Hero2 = namedtuple('Hero2', ('name', 'ru_name', 'en_name', 'image',
                             'role', 'type', 'universe', 'blizz_link',
                             'stats'))

BlizzHero2 = namedtuple('BlizzHero2', ('hero', 'builds'))


class APIParser:

    def __init__(self, data=None):
        self.hero_list = []
        self.json = data

        if data:
            self.parse()

    def parse(self):
        for hero in self.json:
            ru_name_search = dropwhile(lambda name: not is_cyrillic(name),
                                       hero["translations"])
            try:
                ru_name = next(ru_name_search)
            except StopIteration:
                ru_name = ''

            self.hero_list.append(
                ApiHero(hero["name"],
                        ru_name.capitalize(),
                        hero["name"],
                        list(hero["icon_url"].values())[0],
                        hero["role"],
                        hero["type"]))


class BlizzParser2:

    def __init__(self, hero_list=[], page=None):
        self.hero_list = []
        self.bhero_list = []
        self.heroes = hero_list
        self.page = page

        if hero_list and page:
            self.parse()

    def parse(self):
        self.parse_main()

        for hero in self.hero_list[:1]:

            one_hero, its_builds = self.parse_hero_page(self.hero_list[0])
            blizz_hero = BlizzHero2(one_hero, builds=[])

            for build in its_builds:
                talents = self.parse_talents_page(build.link)
                build = Build2(**{**build._asdict(), **{'talents': talents}})

                blizz_hero.builds.append(build)

            print(blizz_hero)

            self.bhero_list.append(blizz_hero)

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

            hero_block = soup.find('a', {'data-name': ru_name})

            if hero_block:

                universe = hero_block.get("data-universe")
                link = hero_block.get("href")

                self.hero_list.append(
                    Hero2(**api_hero._asdict(),
                          universe=universe,
                          blizz_link=link,
                          stats=stats))

    def parse_hero_page(self, hero):
        page = fetch_blizzhero_page('http://blizzardheroes.ru'
                                    + hero.blizz_link)

        soup = BeautifulSoup(page, features="html.parser")
        soup.prettify()

        stats = self.get_stats(soup)
        builds = self.get_builds(soup)

        return Hero2(**{**hero._asdict(), **{'stats': stats}}), builds

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
            link = block.get('href')

            builds.append(Build2(name, [], link))

        return builds

    def parse_talents_page(self, link):
        talents = []
        idx = 0

        page = fetch_blizzhero_page('http://blizzardheroes.ru'
                                    + link)

        soup = BeautifulSoup(page, features="html.parser")
        soup.prettify()

        talent_row = soup.find('div', {'class': 'single-build'})

        for talent in talent_row.find_all('div', {'class': 'single'}):
            level = talent.find('div', {'class': 'single-level'}).text

            talent_info = talent.find('div', {'class': 'single-talent'})

            img = talent_info.find('img')['src']
            name = talent_info.find('div',
                                    {'class': 'tooltipe-talent-title'}).text

            descr = talent_info.find('div',
                                     {'class': 'tooltipe-talent-text'}).text

            talents.append(Talent(idx, level, name, descr, img))

        return talents




    def count_stat(self, bs_obj):
        stat_blocks = bs_obj.find_all('div',
                                      {'class':
                                       'hero-stats-bar active'})

        return len(stat_blocks)
# <a href="/heroes/20-falstad/" class="single" data-role="Убийца" data-universe="warcraft" data-name="фалстад">



#                 <img src="/img/heroes/falstad/icon.jpg" />
#                 <div class="tooltipe tooltipe-hero">
#     <div class="icon">
#         <div><img src="/img/heroes/falstad/hero.jpg" /></div>
#         <div class="game-logo game-logo-warcraft"></div>
#     </div>
#     <div class="desc">
#         <div class="desc-title">­Фалстад</div>
#         <div>­Тан клана Громового молота</div>
#         <div class="desc-role">Роль: Убийца</div>
#         <div class="desc-text">Фалстад Громовой Молот - верховный тан клана Громового Молота и один из основателей Совета Трех Кланов, который ныне заседает в Стальгорне. Несмотря на слухи о его смерти, Фалстад все еще жив-здоров, и вам того желает.</div>
#     </div>
#     <div class="clb"></div>
# </div><br />
#                 <div class="name">Фалстад</div>
#             </a>


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
