import unittest
from parser import HappyParser


class TestParser(unittest.TestCase):

    def test_parse(self):
        hp = HappyParser()
        hp.parse()

        print(hp.hero_list)

    def test_parse_get_name(self):
        hp = HappyParser()
        hp.parse()

        print(hp.take_by_name('Ker'))


if __name__ == '__main__':
    unittest.main()
