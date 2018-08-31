from collections import namedtuple
from functools import partial

from pyrogram.api.types import (InputBotInlineResult,
                                InputBotInlineMessageText)

from pyrogram import (InlineKeyboardMarkup, InlineKeyboardButton)

from data.storage import BLIZZ_HEROES

from utils.filters import take_by_name

from utils.fetcher import fetch_hero_talents
from utils.statistics import fetch_hero_stata, fetch_best_builds

from utils.parser import parse_builds
from utils import pages

from utils.exceptions import *

View = namedtuple('View', ('view'))
Message = namedtuple('Message', ('message'))
MessageList = namedtuple('MessageList', ('messages'))
Markup = namedtuple('Markup', ('message', 'markup'))
Photo = namedtuple('Photo', ('photo', 'caption'))


def send_view(app, user_id, construct_method, *params):
    send_this = construct_method(*params)

    if type(send_this.view) == Message:
        app.send_message(user_id,
                         send_this.view.message)

    elif type(send_this.view) == MessageList:
        for message in send_this.view.messages:
            app.send_message(user_id,
                             message)

    elif type(send_this.view) == Markup:
        app.send_message(user_id,
                         send_this.view.message,
                         reply_markup=send_this.view.markup)

    elif type(send_this.view) == Photo:
        try:
            app.send_photo(
                user_id,
                photo=send_this.view.photo,
                caption=send_this.view.caption
            )
        except Exception as e:
            print(e)
            app.send_message(
                user_id,
                send_this.view.caption
            )
    else:
        raise Exception("Unknown view type.")


def get_hero_profile(name):
    some_heroes, certain_hero = take_by_name(BLIZZ_HEROES, name)

    if not some_heroes:
        message = f'Found no heroes for you :( Is "{name}" hero name correct?'

        view = View(Message(message))

    elif certain_hero:
        bhero = certain_hero

        caption = '**{}**\n__Winrate:{}%__\n```{}```'\
                  .format(bhero.hero.name,

                          fetch_hero_stata(bhero.hero.en_name)
                          .get('percent', '?'),

                          represent_stats(bhero.hero.stats))

        if bhero.hero.image:
            view = View(Photo(bhero.hero.image,
                              caption))
        else:
            view = View(Message(caption))
    else:
        view = View(Markup('Please choose one:',
                           get_hero_variant_buttons(some_heroes)))

    return view


def get_hero_pages(name):
    some_heroes, certain_hero = take_by_name(BLIZZ_HEROES, name)

    page_links = []

    if not some_heroes:
        page_links = []
    elif certain_hero:
        bhero = some_heroes[0]

        best_builds = fetch_best_builds(bhero.hero.en_name)

        best_builds = {'winning': best_builds[0],
                       'popular': best_builds[1]}

        hero_talents = fetch_hero_talents(bhero.hero.en_name)

        builds = parse_builds(hero_talents, best_builds)

        if builds:
            bhero = bhero._replace(builds=builds)

        for build_idx, build in enumerate(bhero.builds):
            page_content = pages.make_page(bhero, build_idx)
            page_link = pages.send_page(bhero.hero.en_name, page_content)

            page_links.append(page_link)
    else:
        page_links = []

    view = View(MessageList(page_links))

    return view


def make_hero_profile(bhero, stata, with_stats=False):

    stats = represent_stats(bhero.hero.stats) if with_stats else ''

    caption = f'**{bhero.hero.name}**\n' \
              + f'__Winrate:{stata.percent}% ' \
              + f'(games: {stata.count}, wins: {stata.win_count})__\n' \
              + f'```{stats}```'

    if bhero.hero.image:
        view = View(Photo(bhero.hero.image,
                          caption))
    else:
        view = View(Message(caption))

    return view


make_short_hero_profile = partial(make_hero_profile, with_stats=False)
make_long_hero_profile = partial(make_hero_profile, with_stats=True)


def get_hero_variant_buttons(some_heroes):
    some_heroes = some_heroes[:5]

    buttons = []

    for bhero in some_heroes:
        buttons.append([InlineKeyboardButton(
                            bhero.hero.name,
                            callback_data=bhero.hero.en_name)])

    return InlineKeyboardMarkup(buttons)


def get_inline_results(query):
    results = []

    some_heroes = take_by_name(BLIZZ_HEROES, query)[:5]

    for idx, bhero in enumerate(some_heroes):
        results.append(
            InputBotInlineResult(
                        id=str(idx),
                        type='article',
                        send_message=InputBotInlineMessageText(
                           bhero.hero.en_name),
                        title=bhero.hero.name,
                        description='{hero.role}\n{hero.stats}'.format(
                            hero=bhero.hero)
            ))

    return results


def represent_stats(stats):
    stats_mapping = {'damage': 'dmg',
                     'utility': 'util',
                     'survivability': 'surv',
                     'complexity': 'cmplx'}

    stats_dict = [('{:<5}'.format(stats_mapping[stat_name]),
                   ' '*(10-stat_value) + '+'*stat_value)
                  for stat_name, stat_value in stats._asdict().items()]

    represent = []

    for idx, stat_part in enumerate(['stats_names', 'stats_values']):
        arr = [stat[idx] for stat in stats_dict]
        transposed = [' '.join(value_row) for value_row
                      in list(map(list, zip(*arr)))]
        represent.append('\n'.join(transposed))

    return '\n-------\n'.join(represent[::-1])
