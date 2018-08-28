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

import chat
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


@app.on_message(Filters.command(["chooseforme", "cfm"]))
def choose_for_me(client, message):
    app.send_message(
        message.chat.id,
        "Well well, wanna chose a hero?",
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    # Generates a callback query when pressed
                    InlineKeyboardButton("Yes", callback_data="choose_0_1"),
                    # Opens a web URL
                    InlineKeyboardButton("No", callback_data="choose_0_0")
                ]
            ]
        )
    )


@app.on_message(Filters.command(["chooseformap", "cfmap"]))
def choose_for_me(client, message):
    ichat.start(app, message.chat.id, "choosebymap")


# @app.on_callback_query(Filters.regex(r"(choosebymap)-(\w+)-(\d+)"))
# def choosebymap_callback(client, message):
#     ichat.receive(app, message.id, message.from_user.id, message.data)


@app.on_callback_query()
def callback(client, message):

    tokens = message.data.split("_")

    if "-" in message.data:
        query_type = "idialog"
    elif len(tokens) == 1:
        query_type = "plain_text"
    elif len(tokens) == 3:
        query_type = "dialog"
    else:
        raise Exception(f"Unknown query: '{message.data}'.")

    if query_type == "plain_text":

        send_hero(message.from_user.id, message.data)

    elif query_type == "dialog":

        dialog_name, reply_cntr, phrase_idx = tokens
        reply_cntr, phrase_idx = int(reply_cntr), int(phrase_idx)

        if reply_cntr == 0:

            if phrase_idx == 1:
                chat.start(app, message.from_user.id, dialog_name)
            elif phrase_idx == 0:
                app.send_message(
                    message.from_user.id,
                    "KK see you next time ^^"
                )
            else:
                print("Unknown error.")

        else:
            chat.send_message(app, message.from_user.id, dialog_name,
                              reply_cntr, phrase_idx)
    elif query_type == 'idialog':
        ichat.receive(app, message.id, message.from_user.id, message.data)
    else:
        raise Exception(f"Unknown query type: '{query_type}'.")


@app.on_message()
def hero_list(client, message):
    send_hero(message.chat.id, message.text)


def send_hero(user_id, in_message):
    views.send_view(app, user_id, views.get_hero_profile, in_message)

    bheroes = filters.take_by_name(storage.BLIZZ_HEROES, in_message)

    if len(bheroes) == 1:
        bhero = bheroes[0]
        for build_idx, build in enumerate(bhero.builds):
            page_content = pages.make_page(bhero, build_idx)
            page_link = pages.send_page(bhero.hero.en_name, page_content)

            app.send_message(
                user_id,
                page_link
            )


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
