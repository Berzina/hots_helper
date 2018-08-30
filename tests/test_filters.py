import pytest
from pprint import pprint

from data_for_test import get_blizz
from utils import filters

BLIZZ_HEROES = []


@pytest.fixture(scope="session", autouse=True)
def auto_session_resource(request):
    global BLIZZ_HEROES

    BLIZZ_HEROES = get_blizz()

    def auto_session_resource_teardown():
        print("auto_session_resource_teardown")
    request.addfinalizer(auto_session_resource_teardown)


@pytest.mark.parametrize("test_input,expected",
                         [("D.Va", ("D.Va", ["D.Va"])),
                          ("Ана", ("Ana", ["Ana", "Sylvanas"])),
                          ("E.T.C.", ("E.T.C.", ["E.T.C."])),
                          ("Art", (None, ["Artanis", "Arthas"]))])
def test_take_by_name(test_input, expected):

    matching, certain_hero = filters.take_by_name(BLIZZ_HEROES, test_input)

    en_name = certain_hero.hero.en_name if certain_hero else None
    matching = [bhero.hero.en_name for bhero in matching]

    print(f"input: {test_input}"
          + f"output: {en_name, matching}, expected: {expected}")

    assert en_name == expected[0]
    assert matching == expected[1]
