import unittest
from utils import filters, views

import data

from data.storage import BLIZZ_HEROES


class TestFilter(unittest.TestCase):

    def setUp(self):
        self.test_data = {0: 1, 1: 4, 2: 1,
                          3: 1, 4: 2, 5: 0}

    def test_by_role(self):
        for bh in filters.by_role(BLIZZ_HEROES, 'warrior'):
            print(bh.role)

    def test_by_choose(self):
        print(views.responce_form(1, self.test_data))
        for bh in filters.by_choose(BLIZZ_HEROES, self.test_data):
            print(bh.hero.name, bh.stats)


if __name__ == '__main__':
    unittest.main()
