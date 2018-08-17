import unittest
from utils import filters

import data

from data.storage import BLIZZ_HEROES


class TestFilter(unittest.TestCase):

    def test_by_role(self):
        for bh in filters.by_role(BLIZZ_HEROES, 'warrior'):
            print(bh.role)

    def test_by_choose(self):
        for bh in filters.by_choose(BLIZZ_HEROES, {0: 1, 1: 4, 2: 1, 3: 1, 4: 2, 5: 0}):
            print(bh.hero.name, bh.stats)


if __name__ == '__main__':
    unittest.main()
