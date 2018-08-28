from collections import namedtuple

from pyrogram.api.types import (InputBotInlineResult,
                                InputBotInlineMessageText)

from pyrogram import (InlineKeyboardMarkup, InlineKeyboardButton)

from data.storage import BLIZZ_HEROES

from utils.filters import take_by_name
from utils.statistics import fetch_hero_stata
from utils.exceptions import *

View = namedtuple('View', ('view'))
Message = namedtuple('Message', ('type', 'message'))
Markup = namedtuple('Markup', ('type', 'message', 'markup'))
Photo = namedtuple('Photo', ('type', 'photo', 'caption'))


def send_view(app, user_id, construct_method, *params):
    send_this = construct_method(*params)

    if send_this.view.type == 'message':
        app.send_message(user_id,
                         send_this.view.message)

    elif send_this.view.type == 'markup':
        app.send_message(user_id,
                         send_this.view.message,
                         reply_markup=send_this.view.markup)

    elif send_this.view.type == 'photo':
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
    some_heroes = take_by_name(BLIZZ_HEROES, name)

    if not some_heroes:
        message = 'Found no heroes for you :( Is "{}" hero name correct?'\
                  .format(name)

        view = View(Message('message',
                            message))

    elif len(some_heroes) == 1:
        bhero = some_heroes[0]

        caption = '**{}**\n__Winrate:{}%__\n```{}```'\
                  .format(bhero.hero.name,

                          fetch_hero_stata(bhero.hero.en_name)
                          .get('percent', '?'),

                          represent_stats(bhero.hero.stats))

        if bhero.hero.image:
            view = View(Photo('photo',
                              bhero.hero.image,
                              caption))
        else:
            view = View(Message('message',
                                caption))
    else:
        view = View(Markup('markup',
                           'Please choose one:',
                           get_hero_variant_buttons(some_heroes)))

    return view


def make_hero_profile(bhero, stata):

    caption = '**{}**\n__Winrate:{}__'\
              .format(bhero.hero.name,

                      "{stata.percent}% (games: {stata.count}, wins: {stata.win_count})"
                      .format(stata=stata))

    if bhero.hero.image:
        view = View(Photo('photo',
                          bhero.hero.image,
                          caption))
    else:
        view = View(Message('message',
                            caption))

    return view


def get_hero_variant_buttons(some_heroes):
    some_heroes = some_heroes[:5]

    buttons = []

    for bhero in some_heroes:
        buttons.append([InlineKeyboardButton(
                            bhero.hero.name,
                            callback_data=bhero.hero.en_name)])

    return InlineKeyboardMarkup(buttons)


def open_build(bh):

    builds_header = '''
* __{}__
```
---------------
 lvl | talent
     | name
---------------```'''

    builds_table = '''```
{:^5}|{}
---------------```
'''

    build_full_table = ''

    for build in bh.builds:
        build_full_table += builds_header.format(build.name)

        for talent in build.talents:
            build_full_table += builds_table.format(talent.level,
                                                    talent.name)

        build_full_table += '\n'

    return '''
**{name}**


{btable}
'''.format(name=bh.hero.name,
           btable=build_full_table)


def link_build(some_heroes):
    response = ''

    for hero in some_heroes:
            response += '''
**{name}**


__Builds:__

{blist}


'''\
.format(name=hero.hero.name,
        blist='\n'.join(['* {bname}: {blink}'
                         .format(bname=build.name,
                                 blink=build.link)
                         for build in hero.builds]))

    return response


def responce_form(user_id, answers):
    from data import dialogs

    questions = dialogs.CHOOSE['questions']
    response = 'You (user {}) responded that:\n'.format(user_id)

    for idx, answer in answers.items():
        if idx:
            field = questions[idx]
            response += '{}: {}\n'.format(field['q'], field['a'][answer])

    return response


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
