import unittest

import data
from data import update
from data.storage import BLIZZ_HEROES


class TestBlizzUpdate(unittest.TestCase):

    def test_update_missing(self):
        update.update_missing()


if __name__ == '__main__':
    unittest.main()
