from data.dialogs import CHOOSE


def take_by_name(happy_heroes, name):
    matching = [hero for hero in happy_heroes
                if name.lower() in hero.name.lower()]

    def match_score(hero):
        ru_pos = hero.ru_name.lower().find(name.lower())
        en_pos = hero.en_name.lower().find(name.lower())

        return ru_pos if ru_pos > en_pos else en_pos

    matching.sort(key=lambda x: match_score(x))

    return matching


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

    stats_mapping = [(stat_name, stat_value)
                     for stat_name, stat_value
                     in stats_mapping
                     if stat_value != 1]  # 1 is for don't care

    stats_mapping.sort(key=lambda stats: stats[1])

    for stat in stats_mapping:
        blizzard_heroes = sorted(blizzard_heroes,
                                 key=lambda bhero:
                                     bhero.stats._asdict()[stat[0]],
                                 reverse=True)

    return blizzard_heroes[:3]
#damage=5, utility=5, survivability=9, complexity=4
