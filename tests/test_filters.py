import pytest
from pprint import pprint

from data_for_test import get_blizz
from utils import filters
from utils.fetcher import fetch_hero_talents

whatever = '*'

BLIZZ_HEROES = []
ALL_HEROES_NAMES = ['Abathur', 'Alarak', "Anub'arak", 'Artanis', 'Arthas',
                    'Auriel', 'Azmodan', 'Brightwing', 'Cassia', 'Chen', 'Cho',
                    'Chromie', 'Dehaka', 'Diablo', 'Falstad', 'Gall',
                    'Garrosh', 'Gazlowe', 'Genji', 'Greymane', "Gul'dan",
                    'Illidan', 'Jaina', 'Johanna', "Kael'thas", 'Kerrigan',
                    'Kharazim', 'Leoric', 'Li Li', 'Li-Ming', 'Lt. Morales',
                    'Lúcio', 'Lunara', 'Malfurion', 'Malthael', 'Medivh',
                    'Muradin', 'Murky', 'Nazeebo', 'Nova', 'Probius',
                    'Ragnaros', 'Raynor', 'Rehgar', 'Rexxar', 'Samuro',
                    'Sgt. Hammer', 'Sonya', 'Stitches', 'Stukov', 'Sylvanas',
                    'Tassadar', 'The Butcher', 'The Lost Vikings', 'Thrall',
                    'Tracer', 'Tychus', 'Tyrael', 'Tyrande', 'Uther',
                    'Valeera', 'Valla', 'Varian', 'Xul', 'Zagara', 'Zarya',
                    'Zeratul', "Zul'jin", "Kel'Thuzad", 'Ana', 'Junkrat',
                    'Alexstrasza', 'Hanzo', 'Blaze', 'Maiev', 'Fenix',
                    'Deckard', 'Yrel', 'Whitemane', 'D.Va', 'E.T.C.']


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
                          ("Art", (None, ["Artanis", "Arthas"])),
                          ("", (None, ALL_HEROES_NAMES))])
def test_take_by_name(test_input, expected):

    matching, certain_hero = filters.take_by_name(BLIZZ_HEROES, test_input)

    en_name = certain_hero.hero.en_name if certain_hero else None
    matching = [bhero.hero.en_name for bhero in matching]

    print(f"input: {test_input}"
          + f"output: {en_name, matching}, expected: {expected}")

    assert en_name == expected[0]
    assert matching == expected[1]


@pytest.fixture(scope="function",
                params=[(("Arthas", "ArthasHeroicAbilitySummonSindragosa"),
                         {'name': 'ArthasHeroicAbilitySummonSindragosa',
                          'title': 'Summon Sindragosa',
                          'description': whatever,
                          'icon': whatever,
                          'icon_url': {},
                          'ability': whatever,
                          'sort': whatever,
                          'cooldown': whatever,
                          'mana_cost': whatever,
                          'level': whatever}),
                        (("Arthas", "BadTalent"),
                         {})],
                ids=["Arthas_existing_talent",
                     "Arthas_non_existing talent"])
def setup_talents_from_api(request):
    hero_name, talent_name = request.param[0]
    expected_output = request.param[1]

    hero_talents = fetch_hero_talents(hero_name)

    return request.param, hero_talents


def test_take_talent_by_name(setup_talents_from_api):
    ((hero_name, talent_name), expected), hero_talents = setup_talents_from_api

    talent = filters.take_talent_by_name(hero_talents, talent_name)

    print(f"\n\nHero: {hero_name},\n"
          f"Hero talent: {talent_name},\n\n"
          f"output: {talent},\n"
          f"expected: {expected}\n")

    for key, value in expected.items():
        assert key in talent

        if type(value) == dict and not value:
            assert type(talent[key]) == dict

        elif type(value) == list and not value:
            assert type(talent[key]) == list

        elif value != whatever:
            assert talent[key] == expected[key]


@pytest.mark.parametrize("test_input,expected",
                         [("warrior", ("Warrior", 20)),
                          ("sup", (None, 0)),
                          ("Warrior", ("Warrior", 20)),
                          ("", (None, 0))])
def test_by_role(test_input, expected):

    heroes = filters.by_role(BLIZZ_HEROES, test_input)
    expected_role, expected_count = expected

    print(f"\n\nRole: {test_input},\n"
          f"Got heroes: {[bhero.hero.name for bhero in heroes]},\n\n"
          f"Their roles: {[bhero.hero.role for bhero in heroes]},\n\n"
          f"Count filtered: {len(heroes)},\n"
          f"Expected count: {expected_count}\n")

    assert all([bhero.hero.role == expected_role for bhero in heroes])
    assert len(heroes) == expected_count


@pytest.mark.parametrize("test_input,expected",
                         [("Я строка", True),
                          ("Я mixed строка", False),
                          ("", False),
                          ("I'm a string", False)])
def test_is_cyrillic(test_input, expected):

    result = filters.is_cyrillic(test_input)

    print(f"\n\nThe string: {test_input},\n"
          f"Expected result: {expected},\n\n"
          f"Got result: {result},\n\n")

    assert expected == result


@pytest.mark.parametrize("test_input,expected",
                         [(["Я строка"], "Я строка"),
                          (["Я строка", "Eщё одна"], "Я строка"),
                          (["Я строка", "Я mixed строка"], "Я строка"),
                          ([], ""),
                          (["I'm a string"], "")])
def test_get_cyrillic(test_input, expected):

    result = filters.get_cyrillic(test_input)

    print(f"\n\nThe strings: {test_input},\n"
          f"Expected result: {expected},\n\n"
          f"Got result: {result},\n\n")

    assert expected == result


@pytest.mark.parametrize("test_input,expected",
                         [("Я строка", "Я строка"),
                          ("Я mixed строка", "Я  строка"),
                          ("", ""),
                          ("&shy;Милосердие", "Милосердие"),
                          ("I'm a string", "'  ")])
def test_get_cyrillic_str(test_input, expected):

    result = filters.get_cyrillic_str(test_input)

    print(f"\n\nThe strings: {test_input},\n"
          f"Expected result: {expected},\n\n"
          f"Got result: {result},\n\n")

    assert expected == result
