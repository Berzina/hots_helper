import random
import re
from itertools import dropwhile

from data.dialogs import CHOOSE


def take_by_name(bheroes, name):
    matching = [bhero for bhero in bheroes
                if name.lower() in bhero.hero.name.lower()]

    def match_score(hero):
        ru_pos = hero.ru_name.lower().find(name.lower())
        en_pos = hero.en_name.lower().find(name.lower())

        return ru_pos if ru_pos > en_pos else en_pos

    matching.sort(key=lambda x: match_score(x.hero))

    return matching


def by_role(blizzard_heroes, role):
    return [bhero for bhero in blizzard_heroes if bhero.hero.role == role]


def by_choose(blizzard_heroes, answers):
    ROLE_MAPPING = CHOOSE['questions'][1]['a']
    STATS = ('damage', 'utility', 'survivability',
             'complexity')

    role_idx = answers[1]

    survivability = answers[2]
    utility = answers[3]
    damage = answers[4]
    complexity = answers[5]

    STATS_VALUES = [survivability, utility, damage, complexity]

    if role_idx != len(ROLE_MAPPING) - 1:
        role = ROLE_MAPPING[role_idx]
        blizzard_heroes = by_role(blizzard_heroes, role)

    stats_mapping = tuple(zip(STATS, STATS_VALUES))

    # 0 is for 'For sure!',
    # 1 is for "Don't care.",
    # 2 is for 'No way!'
    stats_mapping = [(stat_name, stat_value)
                     for stat_name, stat_value
                     in stats_mapping
                     if stat_value != 1]  # 1 is for don't care

    stats_mapping.sort(key=lambda stats: stats[1])

    for stat in stats_mapping:
        reverse = False if stat[1] == 0 else True

        blizzard_heroes = sorted(blizzard_heroes,
                                 key=lambda bhero:
                                     bhero.hero.stats._asdict()[stat[0]],
                                 reverse=reverse)

    blizzard_heroes = blizzard_heroes[:10]
    random.shuffle(blizzard_heroes)

    return blizzard_heroes[:3]
# damage=5, utility=5, survivability=9, complexity=4


# TODO: hardcode range
def is_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))


def get_cyrillic(from_list):
    ru_name_search = dropwhile(lambda name: not is_cyrillic(name),
                               from_list)
    try:
        ru_name = next(ru_name_search)
    except StopIteration:
        ru_name = ''

    return ru_name


def get_cyrillic_str(from_str):
    ru_str_list = list(dropwhile(lambda c: not is_cyrillic(c),
                                 from_str))
    return ''.join(ru_str_list) if ru_str_list else from_str
