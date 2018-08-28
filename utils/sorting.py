def by_cur_winrate(heroes_winrates):

    sorted_by_winrate = sorted(heroes_winrates,
                               key=lambda hero_winrate: hero_winrate.percent,
                               reverse=True)

    return sorted_by_winrate


def by_games_count(heroes_winrates):

    sorted_by_games = sorted(heroes_winrates,
                             key=lambda hero_winrate: hero_winrate.count,
                             reverse=True)

    return sorted_by_games


def by_winrate_count(heroes_winrates):

    sorted_by_games = sorted(heroes_winrates,
                             key=lambda hero_winrate: hero_winrate.win_count,
                             reverse=True)

    return sorted_by_games
