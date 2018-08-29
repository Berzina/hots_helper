from utils.fetcher import fetch_heroes, fetch_blizzhero_page
from utils.parser import APIParser, BlizzParser
from utils.filters import take_by_name

from .storage import set_blizz, BLIZZ_HEROES


def update_all(update_on_loading=True):
    set_blizz([])
    page = fetch_blizzhero_page()
    heroes = APIParser(fetch_heroes()).hero_list
    bheroes = BlizzParser(heroes, page)

    if update_on_loading:
        for hero in heroes:
            set_blizz([bheroes.parse_bhero(hero)], replace=False)
    else:
        set_blizz(bheroes.parse_bhero_list())


def update_missing(update_on_loading=True):
    page = fetch_blizzhero_page()
    heroes = APIParser(fetch_heroes()).hero_list

    missing_heroes = []

    for hero in heroes:
        if not take_by_name(BLIZZ_HEROES, hero.name)[0]:
            missing_heroes.append(hero)

    print("Founded missing heroes:\n{}".format("\n"
                                               .join(
                                    [hero.name for hero in missing_heroes])))

    bheroes = BlizzParser(missing_heroes, page)

    if update_on_loading:
        for hero in missing_heroes:
            set_blizz([bheroes.parse_bhero_by_name(hero.name)], replace=False)
    else:
        set_blizz(bheroes.parse_bhero_list())


def update_concrete(names: list, update_on_loading=True):
    page = fetch_blizzhero_page()
    heroes = APIParser(fetch_heroes()).hero_list

    bheroes = BlizzParser(heroes, page)

    loaded_bheroes = []

    for name in names:
        bhero = bheroes.parse_bhero_by_name(name)
        if update_on_loading:
            set_blizz([bhero], replace=False)
        else:
            loaded_bheroes.append(bhero)

    if not update_on_loading:
        set_blizz(loaded_bheroes)
