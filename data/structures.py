from collections import namedtuple

ApiHero = namedtuple('ApiHero', ('name', 'ru_name', 'en_name', 'image',
                                 'role', 'type'))

Hero = namedtuple('Hero', ('name', 'ru_name', 'en_name', 'image',
                           'role', 'type', 'universe', 'blizz_link',
                           'stats'))

Stats = namedtuple('Stats', ('damage', 'utility', 'survivability',
                             'complexity'))

Build = namedtuple('Build', ('name', 'talents', 'link'))
Build2 = namedtuple('Build2', ('name', 'talents', 'count', 'winrate'))

Talent = namedtuple('Talent', ('idx', 'level', 'name', 'descr', 'img'))
Talent2 = namedtuple('Talent2', ('name', 'title', 'idx', 'level', 'ability',
                                 'descr', 'img'))

BlizzHero = namedtuple('BlizzHero', ('hero', 'builds'))

Stata = namedtuple('Stata', ('hero_name',
                             'percent', 'count', 'win_count',
                             'diff_percent', 'diff_count'))
