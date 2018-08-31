import pytest

from pyrogram import (InlineKeyboardMarkup, InlineKeyboardButton)
from pyrogram.api.types import (InputBotInlineResult,
                                InputBotInlineMessageText)

from pprint import pprint

from utils import statistics, filters

from data.storage import BLIZZ_HEROES

import views

whatever = "*"


@pytest.mark.parametrize("test_input,expected",
                         [("Art", (views.Markup, 'Please choose one:')),
                          ("Arthas", (views.Photo, whatever)),
                          ("Хуйня", (views.Message,
                                     'Found no heroes for you :( '
                                     'Is "Хуйня" hero name correct?'))])
def test_views_get_hero_profile(test_input, expected):

    view = views.get_hero_profile(test_input)
    expected_view_type, expected_message = expected

    print(f"\n\nGiven hero: {test_input} "
          f"Result view type: {type(view.view)}\n"
          f"Expected view type: {expected}\n\n"

          f"Result message: {view.view.message}\n"
          if type(view.view) == views.Message
          or type(view.view) == views.Markup
          else f"Result message: {view.view.caption}\n"

          f"Expected message: {expected_message}\n")

    assert type(view.view) == expected_view_type

    if expected_message != whatever:
        if type(view.view) == views.Message \
          or type(view.view) == views.Markup:
            assert view.view.message == expected_message
        else:
            assert view.view.caption == expected_message


@pytest.mark.parametrize("test_input,expected",
                         [("Art", None),
                          ("Arthas", "Arthas"),
                          ("E.T.C.", "ETC"),
                          ("Хуйня", None)])
def test_views_get_hero_pages(test_input, expected):

    view = views.get_hero_pages(test_input)

    print(f"\n\nGiven hero: {test_input}\n"
          f"Result view type: {type(view.view)}\n"
          f"Expected view type: {views.MessageList}\n\n"

          f"Result pages: {view.view.messages}\n"
          f"Expected message prefix: {expected}\n")

    assert type(view.view) == views.MessageList

    if expected is None:
        assert not view.view.messages
    else:
        assert (len(view.view.messages) == 2
                or len(view.view.messages) == 1)

    assert all([link.startswith(f'https://telegra.ph/{expected}')
                for link in view.view.messages])


@pytest.fixture(scope="function",
                params=[("Arthas", False),
                        ("Хуйня", True)],
                ids=["Arthas", "Хуйня"])
def setup_for_make_profile(request):
    test_input, expect_failure = request.param

    heroes_winrates = statistics.fetch_winrates()

    data = (None, None)

    for hero_winrate in heroes_winrates:
        if hero_winrate.hero_name == test_input:
            _, bhero = filters.take_by_name(BLIZZ_HEROES,
                                            hero_winrate.hero_name)

            data = (bhero, hero_winrate)

    return request.param, data


def test_views_make_hero_profile(setup_for_make_profile):
    (test_input, expect_failure), (bhero, stata) = setup_for_make_profile

    print(f"\n\nGiven hero: {test_input}\n")

    try:
        view = views.make_hero_profile(bhero, stata)

        assert (type(view.view) == views.Message
                or type(view.view) == views.Photo)

        print(f"Result view type: {type(view.view)}\n"
              f"Expected view type: {views.Message} or {views.Photo}\n"

              f"Result message: {view.view.message}\n"
              if type(view.view) == views.Message
              else f"Result message: {view.view.caption}\n")

    except AssertionError as e:
        if not expect_failure:
            raise e
        else:
            print("Get no view and AssertionError as expected.")


@pytest.mark.parametrize("test_input,expected",
                         [(BLIZZ_HEROES[:10], 5),
                          (BLIZZ_HEROES[:5], 5),
                          (BLIZZ_HEROES[:3], 3),
                          ([], 0),
                          pytest.param("Хуйня", 0,
                                       marks=pytest.mark.xfail)])
def test_views_get_hero_variant_buttons(test_input, expected):

    view = views.get_hero_variant_buttons(test_input)

    print(f"\n\nGiven heroes: {[bhero.hero.name for bhero in test_input]}\n"
          f"Result: {view}\n")

    assert type(view) == InlineKeyboardMarkup

    assert all([type(button) == InlineKeyboardButton
                for button_row in view.inline_keyboard
                for button in button_row])

    assert len(view.inline_keyboard) == expected

    idx = 0

    for button_row in view.inline_keyboard:
        for button in button_row:
            assert button.text == test_input[idx].hero.name
            assert button.callback_data == test_input[idx].hero.en_name

            idx += 1


@pytest.mark.parametrize("test_input,expected",
                         [("", ['Abathur', 'Alarak', "Anub'arak",
                                'Artanis', 'Arthas']),
                          ("Арт", ["Artanis", "Arthas"]),
                          ("Керриган", ["Kerrigan"])])
def test_views_get_inline_results(test_input, expected):

    view = views.get_inline_results(test_input)

    print(f"\n\nGiven query: {test_input}\n"
          f"Result: {view}\n")

    assert all([type(inline_result) == InputBotInlineResult
                for inline_result in view])

    for inline_result in view:
        assert inline_result.title.split()[1][1:-1] in expected
