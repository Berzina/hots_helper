from utils.fetcher import fetch_heroes, fetch_blizzhero_page
from utils.parser import APIParser, BlizzParser
from utils.filters import take_by_name

from .storage import set_blizz, BLIZZ_HEROES


def update_all(update_on_loading=True):
    set_blizz([])
    page = fetch_blizzhero_page()
    heroes = APIParser(fetch_heroes()).hero_list
    bheroes = BlizzParser(heroes, page, update_on_loading).bhero_list

    if not update_on_loading:
        set_blizz(bheroes)


def update_missing(update_on_loading=True):
    page = fetch_blizzhero_page()
    heroes = APIParser(fetch_heroes()).hero_list

    missing_heroes = []

    for hero in heroes:
        if not take_by_name(BLIZZ_HEROES, hero.name):
            missing_heroes.append(hero)

    print("Founded missing heroes:\n{}".format("\n"
                                               .join(
                                    [hero.name for hero in missing_heroes])))

    # bheroes = BlizzParser(missing_heroes, page, update_on_loading).bhero_list

    # if not update_on_loading:
    #     set_blizz(bheroes)
