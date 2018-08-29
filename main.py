# -*- coding: utf-8 -*-

import os
import argparse
from pyrogram import (Client, Filters,
                      ReplyKeyboardMarkup,
                      InlineKeyboardMarkup, InlineKeyboardButton)

from pyrogram.api.types import (BotInlineMessageText,
                                MessageEntityBotCommand,
                                InputBotInlineResult,
                                InputBotInlineMessageText,
                                UpdateBotInlineQuery)

from pyrogram.api.functions.messages import (SendInlineBotResult,
                                             SetInlineBotResults)

from dialogs import ichat

from data import update, storage

import views

from utils import pages, filters

SESSIONS = {}

app = Client(os.environ.get('TOKEN'),
             api_id=os.environ.get('API_ID'),
             api_hash=os.environ.get('API_HASH'))


@app.on_message(Filters.command(["start", "help"]))
def hello(client, message):
    client.send_message(
        message.chat.id,
        '''
Hello! I can just teach you how to play a hero
sending you some talents.

Just send me hero name :)''')


@app.on_raw_update()
def raw(client, update, users, chats):
    if isinstance(update, UpdateBotInlineQuery):

        print(f"User '{update.user_id}' sent: '{update.query}'")

        results = views.get_inline_results(update.query)

        if results:
            app.send(SetInlineBotResults(
                        update.query_id,
                        results=results,
                        cache_time=86400
                     ))


@app.on_message(Filters.command(["chooseforquick", "cfq"]))
def choose_for_quick(client, message):
    ichat.start(app, message.chat.id, "chooseforquick")


@app.on_message(Filters.command(["choosefordraft", "cfd"]))
def choose_for_draft(client, message):
    ichat.start(app, message.chat.id, "choosefordraft")


# @app.on_callback_query(Filters.regex(r"(choosebymap)-(\w+)-(\d+)"))
# def choosebymap_callback(client, message):
#     ichat.receive(app, message.id, message.from_user.id, message.data)


@app.on_callback_query()
def callback(client, message):

    if "-" in message.data:
        query_type = "idialog"
    else:
        query_type = "plain_text"

    if query_type == "plain_text":
        send_hero(message.from_user.id, message.data)

    elif query_type == 'idialog':
        ichat.receive(app, message.id, message.from_user.id, message.data)

    else:
        raise Exception(f"Unknown query type: '{query_type}'.")


@app.on_message()
def hero_list(client, message):
    send_hero(message.chat.id, message.text)


def send_hero(user_id, in_message):
    views.send_view(app, user_id, views.get_hero_profile, in_message)
    views.send_view(app, user_id, views.get_hero_pages, in_message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='\
                                        Run the HOTS helper bot\
                                        and update data.')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--updatemissing', action='store_true')
    parser.add_argument('--updateconcrete', nargs='+')

    args = parser.parse_args()

    if args.update:
        update.update_all()
    elif args.updatemissing:
        update.update_missing()
    elif args.updateconcrete:
        update.update_concrete(args.updateconcrete)
    else:
        app.run()
