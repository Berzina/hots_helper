from collections import namedtuple

from pyrogram.api.types import (InputBotInlineResult,
                                InputBotInlineMessageText)

from pyrogram import (InlineKeyboardMarkup, InlineKeyboardButton)

from data.storage import BLIZZ_HEROES
from utils.filters import take_by_name

View = namedtuple('View', ('view'))
Message = namedtuple('Message', ('type', 'message'))
Markup = namedtuple('Markup', ('type', 'message', 'markup'))


def make_view(construct_method, *params):
    view = construct_method(*params)

    if view.view.type == 'message':
        send_this = {'text': view.view.message}
    elif view.view.type == 'markup':
        send_this = {'text': view.view.message,
                     'reply_markup': view.view.markup}
    else:
        raise Exception('Unknown view type.')

    return send_this


def get_hero_view_by_name(name):
    some_heroes = take_by_name(BLIZZ_HEROES, name)

    if not some_heroes:
        message = 'Found no heroes for you :( Is "{}" hero name correct?'\
                  .format(name)

        view = View(Message('message',
                            message))

    elif len(some_heroes) == 1:

        view = View(Message('message',
                            open_build(some_heroes[0])))
    else:
        view = View(Markup('markup',
                           'Please choose one:',
                           get_hero_variant_buttons(some_heroes)))

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
