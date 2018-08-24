import unittest
from utils import filters

import views

from data.storage import BLIZZ_HEROES


class TestFilter(unittest.TestCase):

    def setUp(self):
        self.test_data = {0: 1, 1: 4, 2: 1,
                          3: 1, 4: 2, 5: 0}

    def test_view(self):
        view = views.make_view(views.get_hero_view_by_name,
                               'Арт')

        def fun(text, reply_markup=None):
            print(text)
            print(reply_markup)

        fun(**view)

    def test_view2(self):
        view = views.make_view(views.get_hero_view_by_name,
                               'Артанис')

        def fun(text, reply_markup=None):
            print(text)

        fun(**view)

    def test_view3(self):
        view = views.make_view(views.get_hero_view_by_name,
                               'Хуйня')

        def fun(text, reply_markup=None):
            print(text)

        fun(**view)

    def test_stats(self):
        hero = filters.take_by_name(BLIZZ_HEROES, 'Артас')[0]
        print(views.represent_stats(hero.hero.stats))


if __name__ == '__main__':
    unittest.main()
