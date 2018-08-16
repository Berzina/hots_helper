# -*- coding: utf-8 -*-

import os
import argparse
from pyrogram import Client, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

import data

from utils import views

app = Client(os.environ.get('TOKEN'),
             api_id=os.environ.get('API_ID'),
             api_hash=os.environ.get('API_HASH'))


@app.on_message(Filters.command(["start", "help"]))
def hello(client, message):
    client.send_message(
        message.chat.id,
        '''
Hello! I can just teach you how to play a hero
sending you some talents.''')


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

        app.send_message(
            "me",  # Edit this
            "This is a InlineKeyboardMarkup example",
            reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        # Generates a callback query when pressed
                        InlineKeyboardButton("Button", callback_data="data"),
                        # Opens a web URL
                        InlineKeyboardButton("URL", url="https://docs.pyrogram.ml"),
                    ],
                    [  # Second row
                        # Opens the inline interface of a bot in another chat with a pre-defined query
                        InlineKeyboardButton("Choose chat", switch_inline_query="pyrogram"),
                        # Same as the button above, but the inline interface is opened in the current chat
                        InlineKeyboardButton("Inline here", switch_inline_query_current_chat="pyrogram"),
                    ]
                ]
            )
        )


