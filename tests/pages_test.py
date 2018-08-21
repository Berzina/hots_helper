import unittest

from utils import pages
from utils.filters import take_blizz_by_name


class TestMakingPage(unittest.TestCase):

    def test_view(self):
        bh = take_blizz_by_name('Muradin')
        print(pages.make_page(bh, 0))

    def test_send_page(self):
        bh = take_blizz_by_name('Muradin')
        content = pages.make_page(bh, 0)

        page_link = pages.send_page(bh.hero.en_name, content)

        print(page_link)


if __name__ == '__main__':
    unittest.main()
