import random
import re
from data.dialogs import CHOOSE
from data.storage import HAPPY_HEROES, BLIZZ_HEROES


def take_by_name(happy_heroes, name):
    matching = [hero for hero in happy_heroes
                if name.lower() in hero.name.lower()]

    def match_score(hero):
        ru_pos = hero.ru_name.lower().find(name.lower())
        en_pos = hero.en_name.lower().find(name.lower())

        return ru_pos if ru_pos > en_pos else en_pos

    matching.sort(key=lambda x: match_score(x))

    return matching


def take_blizz_by_name(name):
    some_heroes = take_by_name(HAPPY_HEROES, name)
    try:
        bh = next(bhero for bhero in BLIZZ_HEROES
                  if bhero.hero.name == some_heroes[0].name)

    except StopIteration:
        return 'Hero {name} is not fully updated by some reason.'\
           .format(name)

    return bh


def by_role(blizzard_heroes, role):
    return [bhero for bhero in blizzard_heroes if bhero.role == role]


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
                                     bhero.stats._asdict()[stat[0]],
                                 reverse=reverse)

    blizzard_heroes = blizzard_heroes[:10]
    random.shuffle(blizzard_heroes)

    return blizzard_heroes[:3]
# damage=5, utility=5, survivability=9, complexity=4


# TODO: hardcode range
def is_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))
