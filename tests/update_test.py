import unittest

import data
from data import update
from data.storage import HAPPY_HEROES, BLIZZ_HEROES


class TestBlizzUpdate(unittest.TestCase):

    def test_update_happy(self):
        update.happy_heroes()

    def test_update_missing(self):
        update.missing()


if __name__ == '__main__':
    unittest.main()
