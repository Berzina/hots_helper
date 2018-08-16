import pickle
import os

HAPPY_FILE = 'data/happy.bin'
BLIZZ_FILE = 'data/blizz.bin'

HAPPY_HEROES = []
BLIZZ_HEROES = []

PREFETCHED = {}


def init():
    get_happy()
    get_blizz()


def get_happy():
    global HAPPY_HEROES

    if not HAPPY_HEROES:
        try:
            with open(HAPPY_FILE, 'rb') as fp:
                HAPPY_HEROES = pickle.load(fp)
        except TypeError as e:
            print(e)
            HAPPY_HEROES = []

    return HAPPY_HEROES


def get_blizz():
    global BLIZZ_HEROES

    if not BLIZZ_HEROES:
        try:
            with open(BLIZZ_FILE, 'rb') as fp:
                BLIZZ_HEROES = pickle.load(fp)
        except TypeError:
            BLIZZ_HEROES = []
    return BLIZZ_HEROES


def set_happy(happy_heroes, replace=True):
    global HAPPY_HEROES

    if replace:
        HAPPY_HEROES = happy_heroes
    else:
        for happy_hero in happy_heroes:
            for idx, item in enumerate(HAPPY_HEROES):
                if item.name == happy_hero.name:
                    HAPPY_HEROES[idx] = happy_hero

    if not os.path.isfile(HAPPY_FILE):
        open(HAPPY_FILE, 'w').close()

    with open(HAPPY_FILE, 'wb') as fp:
        pickle.dump(HAPPY_HEROES, fp, fix_imports=True)


def set_blizz(blizz_heroes: list, replace=True):
    global BLIZZ_HEROES

    if replace:
        BLIZZ_HEROES = blizz_heroes
    else:
        for blizz_hero in blizz_heroes:
            for idx, item in enumerate(BLIZZ_HEROES):
                if item.hero.name == blizz_hero.hero.name:
                    BLIZZ_HEROES[idx] = blizz_hero

    if not os.path.isfile(BLIZZ_FILE):
        open(BLIZZ_FILE, 'w').close()

    with open(BLIZZ_FILE, 'wb') as fp:
        pickle.dump(BLIZZ_HEROES, fp, fix_imports=True)


init()
