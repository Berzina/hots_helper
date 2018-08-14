from pyrogram import Client, Filters

app = Client("662893418:AAEMfj8jRYHlYZTTOa4yqzZp9uEDdyyTMDI")


@app.on_message(Filters.text & Filters.private)
def echo(client, message):
    client.send_message(
        message.chat.id, message.text,
        reply_to_message_id=message.message_id
    )


app.run()
