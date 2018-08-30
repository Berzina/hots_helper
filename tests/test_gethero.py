import pytest
from pprint import pprint

import views


def test_get_by_name():

    pprint(views.get_hero_pages("Sylv"))
