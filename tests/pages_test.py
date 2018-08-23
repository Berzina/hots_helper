import unittest

from utils import pages
from utils.filters import take_by_name

from data.storage import BLIZZ_HEROES


class TestMakingPage(unittest.TestCase):

    def test_view(self):
        bh = take_by_name(BLIZZ_HEROES, 'Muradin')[0]
        print(pages.make_page(bh, 0))

    def test_send_page(self):
        bh = take_by_name(BLIZZ_HEROES, 'Muradin')[0]
        content = pages.make_page(bh, 0)

        page_link = pages.send_page(bh.hero.en_name, content)

        print(page_link)


if __name__ == '__main__':
    unittest.main()
