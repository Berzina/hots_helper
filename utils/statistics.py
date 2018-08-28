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


def fetch_stata(build=None, field=None, mode=None):
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

    all_data = fetch_hotsdog("/get-winrates",
                             params)

    return all_data


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


def fetch_winrates(build=None, field=None, mode=None):

    all_stata = fetch_stata(build=None, field=None, mode=None)

    heroes_winrates = []

    if all_stata:
        for hero_name in list(all_stata["Current"].keys()):
            prev = all_stata["Previous"][hero_name]
            current = all_stata["Current"][hero_name]

            prev_count = prev['Losses'] + prev['Wins']
            prev_percent = 100*(prev['Wins']/prev_count)

            current_count = current['Losses'] + current['Wins']
            current_percent = 100*(current['Wins']/current_count)

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
