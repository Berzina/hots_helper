import os
from pyrogram import Client, Filters

import fetcher

app = Client(os.environ.get('TOKEN'))


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
        fetcher.HAPPY_HEROES.prepare_build_response(message.text),
        parse_mode='markdown'
    )


app.run()
