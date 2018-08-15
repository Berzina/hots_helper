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


@app.on_message(Filters.command(["test"]))
def hero_list(client, message):
    some_hero = HAPPY_HEROES.take_by_name('Артас')[0]
    page = fetch_blizz(some_hero.build_refs[0].link)

    bp = BlizzParser(page)

    # client.send_message(
    #     message.chat.id,
    #     fetcher.HAPPY_HEROES.prepare_build_response(message.text),
    # )


app.run()
