import unittest
from utils import filters

import views

from utils.statistics import fetch_init, fetch_winrates
from utils import sorting

from data.storage import BLIZZ_HEROES


class TestFilter(unittest.TestCase):

    def setUp(self):
        self.test_data = {0: 1, 1: 3, 2: 1,
                          3: 1, 4: 2, 5: 0}

        # self.test_data2 = {0: 1, 1: 5, 2: 1,
        #                    3: 1, 4: 2, 5: 0}

    # def test_take_by_name1(self):
    #     hero = filters.take_by_name(BLIZZ_HEROES, 'D.Va')

    #     print(views.open_build(hero[0]))

    # def test_take_by_name(self):
    #     heroes = filters.take_by_name(BLIZZ_HEROES, 'Мора')
    #     print(heroes)

    #     print(views.link_build(heroes))

    # def test_by_role(self):
    #     for bh in filters.by_role(BLIZZ_HEROES, 'warrior'):
    #         print(bh.hero.role)

    # def test_by_choose(self):
    #     # print(views.responce_form(1, self.test_data))
    #     for bh in filters.by_choose(BLIZZ_HEROES, self.test_data):
    #         print(bh.hero.name, bh.hero.stats)

    def test_by_map(self):
        init_data = fetch_init()

        map_idx = input("Choose map:\n{}\n"
                        .format("\n"
                                .join([f"{idx}: {map_name}"
                                       for idx, map_name
                                       in enumerate(init_data["maps"])])))

        heroes_winrates = fetch_winrates(init_data["maps"][int(map_idx)])

        sorted_heroes_winrate = sorting.by_cur_winrate(heroes_winrates)

        for hero_winrate in sorted_heroes_winrate[:5]:
            some_heroes = filters.take_by_name(BLIZZ_HEROES, hero_winrate[0])

            if some_heroes and len(some_heroes) == 1:

                print(some_heroes[0].hero.name)
                print(hero_winrate)

        print("*"*50)

        sorted_heroes_count = sorting.by_games_count(heroes_winrates)

        for hero_winrate in sorted_heroes_count[:5]:
            some_heroes = filters.take_by_name(BLIZZ_HEROES, hero_winrate[0])

            if some_heroes and len(some_heroes) == 1:

                print(some_heroes[0].hero.name)
                print(hero_winrate)


if __name__ == '__main__':
    unittest.main()
