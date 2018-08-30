import pytest
from pprint import pprint

import data
from data import update
from data.storage import BLIZZ_HEROES


def test_update_missing():
    update.update_missing()
