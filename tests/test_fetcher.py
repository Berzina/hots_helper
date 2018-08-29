import pytest
from pprint import pprint

from data.storage import BLIZZ_HEROES
from utils.statistics import fetch_best_builds
from utils.fetcher import fetch_hero_talents


def test_fetch():
    bhero = BLIZZ_HEROES[0]

    pprint(fetch_best_builds(bhero.hero.en_name), indent=4)


def test_fetch_talents():
    bhero = BLIZZ_HEROES[0]

    pprint(fetch_hero_talents(bhero.hero.en_name), indent=4)
