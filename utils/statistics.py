from collections import namedtuple
from .fetcher import fetch_hotsdog

Stata = namedtuple('Stata', ('hero_name',
                             'percent', 'count', 'win_count',
                             'diff_percent', 'diff_count'))


def fetch_init():
    all_data = fetch_hotsdog("/init")

    if all_data:
        build = all_data["Builds"][0]["ID"]
        maps = all_data["Maps"]
        modes = all_data["Modes"]

        return {'build': all_data["Builds"][0]["ID"],
                'maps': all_data["Maps"],
                'modes': all_data["Modes"]}


def fetch_stata(build=None, field=None, mode=None,
                skill_low=None, skill_high=None):

    params = construct_params(build, field, mode, skill_low, skill_high)

    all_data = fetch_hotsdog("/get-winrates",
                             params)

    return all_data


def construct_params(build=None, field=None, mode=None, hero=None,
                     skill_low=None, skill_high=None):

    if not build:
        init_data = fetch_init()
        if init_data:
            build = init_data["build"]
        else:
            raise Exception("Cannot fetch data without build.")

    params = {"build": build}

    if field:
        params.update({"map": field})
    if mode:
        params.update({"mode": mode})
    if hero:
        params.update({"hero": hero})
    if skill_low:
        params.update({"skill_low": skill_low})
    if skill_high:
        params.update({"skill_high": skill_high})

    return params


def fetch_hero_stata(hero_name, build=None, field=None, mode=None):

    all_data = fetch_stata(build, field, mode)

    if all_data:
        prev = all_data["Previous"][hero_name]
        current = all_data["Current"][hero_name]

        prev_count = prev['Losses'] + prev['Wins']
        prev_percent = 100*(prev['Wins']/prev_count)

        current_count = current['Losses'] + current['Wins']
        current_percent = 100*(current['Wins']/current_count)

        diff_percent = current_percent - prev_percent
        diff_count = current_count - prev_count

        return {'percent': round(current_percent, 2),
                'count': current_count,
                'diff_percent': round(diff_percent, 2),
                'diff_count': diff_count}

    return {}


def fetch_build_winrates(hero_name, build=None, field=None, mode=None):
    params = construct_params(build, field, mode, hero_name)

    all_data = fetch_hotsdog("/get-build-winrates",
                             params)

    return all_data


def fetch_best_builds(hero_name, build=None, field=None, mode=None):

    most_popular = {}
    most_winning = {}

    all_data = fetch_build_winrates(hero_name, build, field, mode)

    if "PopularBuilds" in all_data and all_data["PopularBuilds"] is not None:
        most_popular = sorted(all_data["PopularBuilds"],
                              key=lambda build: build['Total'],
                              reverse=True)[0]

    if "WinningBuilds" in all_data and all_data["WinningBuilds"] is not None:
        most_winning = sorted(all_data["WinningBuilds"],
                              key=lambda build: build['Winrate'],
                              reverse=True)[0]

    return most_winning, most_popular


def fetch_winrates(build=None, field=None, mode=None,
                   skill_low=None, skill_high=None):

    all_stata = fetch_stata(build, field, mode,
                            skill_low, skill_high)

    heroes_winrates = []

    if all_stata:
        for hero_name in list(all_stata["Current"].keys()):
            default = {'Wins': 0, 'Losses': 0}

            prev = all_stata["Previous"].get(hero_name, default)
            current = all_stata["Current"].get(hero_name, default)

            prev_count = prev['Losses'] + prev['Wins']
            prev_percent = 100*(prev['Wins']/prev_count) if prev_count else 0

            current_count = current['Losses'] + current['Wins']
            current_percent = 100*(current['Wins']/current_count) if current_count else 0

            diff_percent = current_percent - prev_percent
            diff_count = current_count - prev_count

            stata = Stata(hero_name=hero_name,
                          percent=round(current_percent, 2),
                          win_count=current['Wins'],
                          count=current_count,
                          diff_percent=round(diff_percent, 2),
                          diff_count=diff_count)

            heroes_winrates.append(stata)

    return heroes_winrates
