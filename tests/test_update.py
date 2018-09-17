import pytest
from pprint import pprint

import data
from data import update
from data.storage import BLIZZ_HEROES


@pytest.mark.skip(reason="Tested and ok")
def test_update_missing():
    update.update_missing()


def test_update_concrete():
    update.update_concrete(['Whitemane'])
