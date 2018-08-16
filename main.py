# -*- coding: utf-8 -*-

import os
import argparse
from pyrogram import Client, Filters, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

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


@app.on_message(Filters.command(["chooseforme"]))
def choose_for_me(client, message):
    app.send_message(
        message.chat.id,
        "Well well, wanna chose a hero?",
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    # Generates a callback query when pressed
                    InlineKeyboardButton("Yes", callback_data="choose1"),
                    # Opens a web URL
                    InlineKeyboardButton("No", callback_data="choose0")
                ]
            ]
        )
    )


@app.on_callback_query()
def choose_1(client, message):

    if message.data == "choose0":
        reply = "KK goodbye then."
    elif message.data == "choose1":
        reply = "Well it will be done one day. Just choose by yoursef now :)"
    else:
        reply = "Unknown"

    app.send_message(
        message.from_user.id,
        "Well it will be done one day. Just choose by yoursef now :)"
    )


@app.on_message()
def hero_list(client, message):
    client.send_message(
        message.chat.id,
        views.get_hero_view_by_name(message.text)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='\
                                        Run the HOTS helper bot\
                                        and update data.')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--updatemissing', action='store_true')

    args = parser.parse_args()

    if args.update:
        data.update.data()
    elif args.updatemissing:
        data.update.missing()
    else:
        app.run()


