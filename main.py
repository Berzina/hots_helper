# -*- coding: utf-8 -*-

import os
from pyrogram import Client, Filters

import fetcher

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
        fetcher.get_hero_view_by_name(message.text)
    )


app.run()
