import unittest
from views import get_hero_view_by_name
from utils.parser import BlizzParser

import data


# class TestHeroParser(unittest.TestCase):

#     def test_all_heroes(self):
#         for hero in get_happy():
#             print(hero)


class TestBlizzParser(unittest.TestCase):

    def test_view(self):
        print(get_hero_view_by_name("Моралес"))

    def test_prefetch_view(self):
        print(get_hero_view_by_name("Лунара"))

    def test_prefetch_view2(self):
        print(get_hero_view_by_name("Вариан"))

    def test_prefetch_view3(self):
        print(get_hero_view_by_name("Силь"))


if __name__ == '__main__':
    unittest.main()
