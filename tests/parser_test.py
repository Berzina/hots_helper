import unittest
from fetcher import HAPPY_HEROES, fetch_data, update_heroes, fetch_blizz
from utils.parser import BlizzParser


# class TestHeroParser(unittest.TestCase):

#     def setUp(self):
#         fetch_data()
#         update_heroes()

#     # def test_parse(self):
#     #     print(fetcher.HAPPY_HEROES.hero_list)

#     # def test_parse_get_name(self):
#     #     print(fetcher.HAPPY_HEROES.take_by_name('Ker'))

#     # def test_parse_with_Response(self):
#     #     print(fetcher.HAPPY_HEROES.prepare_build_response('Ana'))

#     def test_parse_with_Response2(self):
#         print(HAPPY_HEROES.prepare_build_response('Ar'))


class TestBlizzParser(unittest.TestCase):
    def setUp(self):
        fetch_data()
        update_heroes()

    def test_fetch_page_with_talents(self):
        some_hero = HAPPY_HEROES.take_by_name('Артас')[0]
        page = fetch_blizz(some_hero.build_refs[0].link)

        bp = BlizzParser(page)


if __name__ == '__main__':
    unittest.main()
