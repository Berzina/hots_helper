import unittest
from parser import HappyParser


class TestParser(unittest.TestCase):

    def test_parse(self):
        hp = HappyParser()
        hp.parse()

        print(hp.hero_list)


if __name__ == '__main__':
    unittest.main()
