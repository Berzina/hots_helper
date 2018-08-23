import unittest
from utils import filters

import views

from data.storage import BLIZZ_HEROES


class TestFilter(unittest.TestCase):

    def setUp(self):
        self.test_data = {0: 1, 1: 4, 2: 1,
                          3: 1, 4: 2, 5: 0}

    def test_view(self):
        print(views.get_hero_view_by_name('Арт'))

    def test_view2(self):
        print(views.get_hero_view_by_name('Артанис'))

    def test_view3(self):
        print(views.get_hero_view_by_name('Хуйня'))


if __name__ == '__main__':
    unittest.main()
