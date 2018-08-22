import unittest

from utils.fetcher import fetch_statistics


class TestFetchStata(unittest.TestCase):

    def test_raw_fetch(self):
        print(fetch_statistics())


if __name__ == '__main__':
    unittest.main()
