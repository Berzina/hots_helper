import pickle
import os

MAP_NAMES = ['Alterac Pass', 'Battlefield of Eternity', "Blackheart's Bay",
             'Braxis Holdout', 'Cursed Hollow', 'Dragon Shire',
             'Garden of Terror', 'Hanamura', 'Haunted Mines',
             'Industrial District', 'Infernal Shrines', 'Sky Temple',
             'Tomb of the Spider Queen', 'Towers of Doom',
             'Volskaya Foundry', 'Warhead Junction']

BLIZZ_FILE = os.path.join(
                 os.path.dirname(
                    os.path.abspath(__file__)),
                 'blizz.bin'
             )

BLIZZ_HEROES = []


def init():
    get_blizz()
    # for bhero in BLIZZ_HEROES:
    #     print(bhero.hero.name)


def get_blizz():
    global BLIZZ_HEROES

    if not os.path.isfile(BLIZZ_FILE):
        open(BLIZZ_FILE, 'w').close()

    if not BLIZZ_HEROES:
        try:
            with open(BLIZZ_FILE, 'rb') as fp:
                BLIZZ_HEROES = pickle.load(fp)
        except (TypeError, EOFError):
            BLIZZ_HEROES = []
    return BLIZZ_HEROES


def set_blizz(blizz_heroes: list, replace=True):
    global BLIZZ_HEROES

    if replace:
        BLIZZ_HEROES = [bhero for bhero in blizz_heroes if bhero]
    else:
        for blizz_hero in blizz_heroes:
            founded = False
            for idx, item in enumerate(BLIZZ_HEROES):

                if blizz_hero \
                   and ((blizz_hero.hero.ru_name != ''
                         and item.hero.ru_name == blizz_hero.hero.ru_name)
                        or item.hero.en_name == blizz_hero.hero.en_name):

                    founded = True

                    print(f'Hero ru name matched: '
                          f'{item.hero.ru_name == blizz_hero.hero.ru_name}')

                    print(f'Hero en name is mathing: '
                          f'{item.hero.en_name == blizz_hero.hero.en_name}')

                    print(f'Replacing: {BLIZZ_HEROES[idx].hero.name}')

                    BLIZZ_HEROES[idx] = blizz_hero

                    print("\nAdded heroes: \n{}\nwas loaded to bin.\n"
                          .format(", ".join([bhero.hero.name
                                             for bhero in blizz_heroes])))

                    print("\nAll heroes: \n{}\nwas loaded to bin.\n"
                          .format(", ".join([bhero.hero.name
                                             for bhero in BLIZZ_HEROES])))

        if not founded and blizz_hero:
            BLIZZ_HEROES.append(blizz_hero)

    if not os.path.isfile(BLIZZ_FILE):
        open(BLIZZ_FILE, 'w').close()

    with open(BLIZZ_FILE, 'wb') as fp:
        pickle.dump(BLIZZ_HEROES, fp, fix_imports=True)


init()
