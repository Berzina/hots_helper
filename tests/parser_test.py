import unittest
import fetcher


class TestParser(unittest.TestCase):

    # def test_parse(self):
    #     print(fetcher.HAPPY_HEROES.hero_list)

    # def test_parse_get_name(self):
    #     print(fetcher.HAPPY_HEROES.take_by_name('Ker'))

    # def test_parse_with_Response(self):
    #     print(fetcher.HAPPY_HEROES.prepare_build_response('Ana'))

    def test_parse_with_Response2(self):
        print(fetcher.HAPPY_HEROES.prepare_build_response('Ar'))


if __name__ == '__main__':
    unittest.main()
