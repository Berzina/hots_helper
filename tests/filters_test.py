import unittest
from utils import filters

import views

from data.storage import BLIZZ_HEROES


class TestFilter(unittest.TestCase):

    def setUp(self):
        self.test_data = {0: 1, 1: 4, 2: 1,
                          3: 1, 4: 2, 5: 0}

    def test_take_by_name(self):
        hero = filters.take_by_name(BLIZZ_HEROES, 'Abathur')

        print(views.open_build(hero[0]))

    def test_by_role(self):
        for bh in filters.by_role(BLIZZ_HEROES, 'warrior'):
            print(bh.hero.role)

    def test_by_choose(self):
        print(views.responce_form(1, self.test_data))
        for bh in filters.by_choose(BLIZZ_HEROES, self.test_data):
            print(bh.hero.name, bh.hero.stats)

            print(bh)


if __name__ == '__main__':
    unittest.main()
