import os
import pickle

BLIZZ_FILE = os.path.join(
                 os.path.dirname(
                    os.path.abspath(__file__)),
                 'test_blizz_heroes.bin'
             )


def get_blizz():

    if not os.path.isfile(BLIZZ_FILE):
        open(BLIZZ_FILE, 'w').close()

    try:
        with open(BLIZZ_FILE, 'rb') as fp:
            BLIZZ_HEROES = pickle.load(fp)
    except (TypeError, EOFError):
        BLIZZ_HEROES = []

    return BLIZZ_HEROES
