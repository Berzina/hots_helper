import pytest
from pprint import pprint

from utils.statistics import *


@pytest.mark.skip(reason="Tested and good.")
def test_fetch_all_stata():

    pprint(fetch_stata())


def test_fetch_build_winrate():
    data = fetch_build_winrates("Sylv")

    pprint(data.get("WinningBuilds", {}))
    pprint(data.get("PopularBuilds", {}))
