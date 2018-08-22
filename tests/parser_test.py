import unittest
from views import get_hero_view_by_name
from utils.parser import BlizzParser, APIParser, BlizzParser2
from utils.fetcher import fetch_heroes, fetch_blizzheroes_page

import data


# class TestHeroParser(unittest.TestCase):

#     def test_all_heroes(self):
#         for hero in get_happy():
#             print(hero)


# class TestBlizzParser(unittest.TestCase):

#     def test_view(self):
#         print(get_hero_view_by_name("Моралес"))

#     def test_prefetch_view(self):
#         print(get_hero_view_by_name("Лунара"))

#     def test_prefetch_view2(self):
#         print(get_hero_view_by_name("Вариан"))

#     def test_prefetch_view3(self):
#         print(get_hero_view_by_name("Силь"))


class TestApiParse(unittest.TestCase):

    # def test_parse(self):
    #     print(APIParser(fetch_heroes()).hero_list)

    def test_fetch(self):
        page = fetch_blizzheroes_page()
        heroes = APIParser(fetch_heroes()).hero_list

        print(BlizzParser2(heroes, page).bhero_list)


if __name__ == '__main__':
    unittest.main()
