import unittest

from utils.statistics import *


class TestFetchStata(unittest.TestCase):

    def test_raw_fetch(self):
        print(fetch_init())

    def test_fetch_stata(self):
        print(fetch_stata())

    def test_fetch_hero_stata(self):
        print(fetch_hero_stata("Arthas"))


if __name__ == '__main__':
    unittest.main()
