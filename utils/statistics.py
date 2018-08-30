from collections import namedtuple, Counter
from pprint import pprint
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
        builds = []

        majore, minore, bagofix = build.split(".")
        bagofix = int(bagofix)

        start_version = bagofix - 3 if bagofix >= 3 else 0
        end_version = bagofix + 1

        for fixver in range(start_version, end_version):
            builds.append(f"{majore}.{minore}.{bagofix}")

        return {'build': build,
                'builds': builds,
                'maps': maps,
                'modes': modes}


def fetch_stata(field=None, mode=None,
                skill_low=None, skill_high=None):

    params, builds = construct_params(field, mode, skill_low, skill_high)

    all_data = {}

    for build in builds:
        params.update({"build": build})
        part_data = fetch_hotsdog("/get-winrates",
                                  params)

        if not all_data:
            all_data = part_data
        else:
            for time, heroes in part_data.items():
                for hero in heroes:
                    all_data[time].update(
                        {hero:
                         dict(Counter(all_data[time][hero])
                         + Counter(part_data[time][hero]))})

    return all_data


def construct_params(field=None, mode=None, hero=None,
                     skill_low=None, skill_high=None):

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

    return params, init_data["builds"]


def fetch_hero_stata(hero_name, build=None, field=None, mode=None):

    all_data = fetch_stata(field, mode)

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


def fetch_build_winrates(hero_name, field=None, mode=None):
    params, builds = construct_params(field, mode, hero_name)

    all_data = {}

    for build in builds:
        params.update({"build": build})
        part_data = fetch_hotsdog("/get-build-winrates",
                                  params)

        if not all_data:
            all_data = part_data
        else:
            for wanted_build in ["PopularBuilds", "WinningBuilds"]:
                if wanted_build not in part_data \
                   or part_data[wanted_build] is None:
                    continue
                elif wanted_build not in all_data \
                     and wanted_build in part_data:
                    all_data.update({wanted_build: part_data[wanted_build]})
                else:
                    all_data[wanted_build] \
                    += part_data[wanted_build]

    return all_data


def fetch_best_builds(hero_name, field=None, mode=None):

    most_popular = {}
    most_winning = {}

    all_data = fetch_build_winrates(hero_name, field, mode)

    if "PopularBuilds" in all_data and all_data["PopularBuilds"] is not None:
        most_popular = sorted(all_data["PopularBuilds"],
                              key=lambda build: build['Winrate'],
                              reverse=True)

        most_popular = sorted(most_popular,
                              key=lambda build: build['Total'],
                              reverse=True)[0]

    if "WinningBuilds" in all_data and all_data["WinningBuilds"] is not None:
        most_winning = sorted(all_data["WinningBuilds"],
                              key=lambda build: build['Winrate'],
                              reverse=True)[0]

    return most_winning, most_popular


def fetch_winrates(field=None, mode=None,
                   skill_low=None, skill_high=None):

    all_stata = fetch_stata(field, mode,
                            skill_low, skill_high)

    heroes_winrates = []

    if all_stata:
        for hero_name in list(all_stata["Current"].keys()):
            default = {'Wins': 0, 'Losses': 0}

            prev = all_stata["Previous"].get(hero_name, default)
            pprint(all_stata["Previous"].get(hero_name, default))
            current = all_stata["Current"].get(hero_name, default)

            prev_count = prev.get('Losses', 0) + prev.get('Wins', 0)
            prev_percent = 100*(prev.get('Wins', 0)/prev_count) \
                           if prev_count else 0

            current_count = current.get('Losses', 0) + current.get('Wins', 0)
            current_percent = 100*(current.get('Wins', 0)/current_count) \
                              if current_count else 0

            diff_percent = current_percent - prev_percent
            diff_count = current_count - prev_count

            stata = Stata(hero_name=hero_name,
                          percent=round(current_percent, 2),
                          win_count=current.get('Wins', 0),
                          count=current_count,
                          diff_percent=round(diff_percent, 2),
                          diff_count=diff_count)

            heroes_winrates.append(stata)

    return heroes_winrates
