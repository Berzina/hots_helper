import pytest
from pprint import pprint

from data.storage import BLIZZ_HEROES

from utils import fetcher


# def test_basic_fetch():
#     response = fetcher.basic_fetch('http://hotsapi.net/api/v1/',
#                                    appendix='heroes')

#     pprint(response, indent=4)


def test_fetch_hero_talents():
    response = fetcher.fetch_hero_talents('Mephisto')

    pprint(response, indent=4)
