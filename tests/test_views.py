import pytest
from pprint import pprint

import views


@pytest.mark.parametrize("test_input,expected",
                         [("Art", ("D.Va", ["D.Va"])),
                          ("Arthas", ("Ana", ["Ana", "Sylvanas"])),
                          ("Хуйня", ("E.T.C.", ["E.T.C."]))])
def test_views_get_hero_profile(test_input, expected):

    view = views.get_hero_profile(test_input)

    print(f"input: {test_input} "
          f"output: {view}, expected: {expected}")

    if type(view.view) == views.Markup:
        print(view.view.markup)

    assert type(view) == views.View
