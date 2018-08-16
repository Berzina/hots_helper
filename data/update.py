from utils.fetcher import fetch_data, fetch_blizz, fetch_blizz_hero
from utils.parser import HappyParser

from .storage import (set_happy, set_blizz, get_happy,
                      HAPPY_HEROES, BLIZZ_HEROES)


def happy_heroes():
    HAPPY_HEROES = HappyParser(fetch_data()).hero_list
    set_happy(HAPPY_HEROES)


def blizz_heroes(hero=None):
    if not hero:
        HAPPY_HEROES = get_happy()
        set_blizz(fetch_blizz(HAPPY_HEROES))
    else:
        new_blizz = fetch_blizz_hero(hero)
        set_blizz([new_blizz], replace=False)


def missing():
    missing_blizz_heroes()
    missing_blizz_talents()


def missing_blizz_heroes():
    for hero in HAPPY_HEROES:
        try:
            bh = next(bhero for bhero in BLIZZ_HEROES
                      if bhero.hero.name == hero.name)

        except StopIteration:
            blizz_heroes(hero)


def missing_blizz_talents():
    for bhero in BLIZZ_HEROES:
        for build in bhero.builds:
            if not build.talents:
                blizz_heroes(bhero.hero)


def data():
    happy_heroes()
    blizz_heroes()
