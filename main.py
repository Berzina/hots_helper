# -*- coding: utf-8 -*-

import os
import argparse
from pyrogram import (Client, Filters,
                      ReplyKeyboardMarkup,
                      InlineKeyboardMarkup, InlineKeyboardButton)

from pyrogram.api.types import (BotInlineMessageText,
                                MessageEntityBotCommand,
                                InputBotInlineResult,
                                InputBotInlineMessageText)

from pyrogram.api.functions.messages import SendInlineBotResult

import chat

import data

from utils import views

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


@app.on_message(Filters.regex("test_inline"))
def inline(client, message):
    app.send(
        SetInlineBotResults(query_id=0,
                            results=[
                              InputBotInlineResult(
                                id="0",
                                type='message',
                                send_message=InputBotInlineMessageText('hello')
                              )
                            ])
        )


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


@app.on_callback_query()
def callback(client, message):

    dialog_name, reply_cntr, phrase_idx = message.data.split("_")
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
        chat.send_message(app, message.from_user.id, dialog_name, reply_cntr,
                          phrase_idx)


@app.on_message()
def hero_list(client, message):
    client.send_message(
        message.chat.id,
        views.get_hero_view_by_name(message.text)
    )


def send_text(user_id, text):
    app.send_message(
            user_id,
            "Hey smth is broken, sorry friend ^^'"
        )


def send_keyboard(user_id, header, keyboard):
    app.send_message(
        user_id,
        header,
        reply_markup=keyboard
    )


def get_app():
    return app


app.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='\
                                        Run the HOTS helper bot\
                                        and update data.')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--updatemissing', action='store_true')

    args = parser.parse_args()

    if args.update:
        app.stop()
        data.update.data()
    elif args.updatemissing:
        app.stop()
        data.update.missing()
    else:
        pass
