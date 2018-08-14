from pyrogram import Client, Filters


from parser import HappyParser

app = Client("662893418:AAEMfj8jRYHlYZTTOa4yqzZp9uEDdyyTMDI")


@app.on_message(Filters.command(["start", "help"]))
def hello(client, message):
    client.send_message(
        message.chat.id,
        '''
        Hello! I can just teach you how to play a hero
        sending you some talents.
        ''')


@app.on_message()
def hero_list(client, message):
    hp = HappyParser()
    hp.parse()

    client.send_message(
        message.chat.id,
        hp.prepare_build_response(message.text),
        parse_mode='markdown'
    )


app.run()
